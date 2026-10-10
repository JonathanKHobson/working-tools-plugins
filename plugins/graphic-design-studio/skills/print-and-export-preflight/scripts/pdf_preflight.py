#!/usr/bin/env python3
"""Inspect local PDF mechanics; never equate a pass with visual/press approval."""
import argparse
import json
import math
import sys
from pathlib import Path


def positive(value):
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise argparse.ArgumentTypeError('must be a finite positive number')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--size-in', nargs=2, type=positive, metavar=('WIDTH', 'HEIGHT'))
    parser.add_argument('--max-mb', type=positive, help='decimal MB')
    parser.add_argument('--min-type-pt', type=positive)
    parser.add_argument('--min-ppi', type=positive)
    parser.add_argument('--require-text', action='append', default=[])
    parser.add_argument('--qr', action='append', default=[], help='expected unique payload; repeat for multiple')
    parser.add_argument('--dpi', type=positive, default=120)
    parser.add_argument('--render-dir', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not 1 <= args.dpi <= 600:
        parser.error('--dpi must be between 1 and 600 to bound preview memory use')
    if args.report and args.report.resolve() == args.pdf.resolve():
        parser.error('--report must not overwrite the input PDF')
    report = {'file': str(args.pdf.resolve()), 'checks': [], 'pages': [],
              'limitations': [
                  'Mechanical checks only; rendered visual QA is separate.',
                  'Color, PDF/X, font embedding/licensing, rights and approval are not certified.',
                  'Text bounds use the visible page; frame-safe margins and bleed need separate inspection.',
                  'Extracted text misses outlined/raster type and can miss hidden, overlapping or fully clipped text.',
                  'Image PPI reflects embedded pixels, not pre-upsampling source detail.',
                  'Software QR decoding is not a live URL check or physical phone scan.']}

    def check(name, status, detail):
        report['checks'].append({'check': name, 'status': status, 'detail': detail})

    def finish():
        statuses = {c['status'] for c in report['checks']}
        result = 1 if 'fail' in statuses else 2 if 'unavailable' in statuses else 0
        report['result'] = {0: 'requested-mechanical-checks-pass',
                            1: 'mechanical-check-failure',
                            2: 'requested-check-unavailable'}[result]
        payload = json.dumps(report, indent=2)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(payload + '\n')
        print(payload)
        return result

    try:
        import fitz
    except ImportError:
        check('runtime', 'unavailable', 'PyMuPDF required; use an existing suitable Python runtime.')
        return finish()
    try:
        doc = fitz.open(args.pdf)
        if not doc.is_pdf or doc.needs_pass or len(doc) == 0:
            check('document', 'unavailable', 'Expected a readable, nonempty, unencrypted PDF.')
            return finish()
    except Exception as exc:
        check('document', 'unavailable', str(exc))
        return finish()
    bytes_count = args.pdf.stat().st_size
    report['bytes'] = bytes_count
    if args.max_mb:
        check('file-size', 'pass' if bytes_count <= args.max_mb * 1_000_000 else 'fail',
              {'actual_mb': round(bytes_count / 1_000_000, 4), 'maximum_mb': args.max_mb})
    decoder = None
    if args.qr:
        try:
            from PIL import Image
            import zxingcpp
            decoder = (Image, zxingcpp)
        except ImportError:
            check('qr-runtime', 'unavailable', 'Pillow and zxing-cpp required for requested QR check.')
    if args.render_dir:
        args.render_dir.mkdir(parents=True, exist_ok=True)
    all_text, payloads = [], set()
    for index, page in enumerate(doc):
        tag = f'page-{index + 1}'
        row = {'page': index + 1, 'inches': [round(page.rect.width / 72, 4),
                                           round(page.rect.height / 72, 4)]}
        report['pages'].append(row)
        if args.size_in:
            ok = all(abs(actual - target) <= .01 for actual, target in zip(row['inches'], args.size_in))
            check(tag + '-size', 'pass' if ok else 'fail', row['inches'])
        spans = [s for b in page.get_text('dict')['blocks'] if b['type'] == 0
                 for line in b['lines'] for s in line['spans'] if s['text'].strip()]
        text = page.get_text()
        all_text.append(text)
        row['extracted_text_characters'] = len(text)
        row['minimum_extracted_type_pt'] = round(min((s['size'] for s in spans), default=0), 2)
        if args.min_type_pt:
            status = 'unavailable' if not spans else 'pass' if min(s['size'] for s in spans) >= args.min_type_pt - .01 else 'fail'
            check(tag + '-type-size', status, row['minimum_extracted_type_pt'])
        if page.rotation:
            check(tag + '-text-bounds', 'unavailable', 'Rotated page requires manual bounds inspection.')
        else:
            bounds = fitz.Rect(page.rect.x0 - .5, page.rect.y0 - .5, page.rect.x1 + .5, page.rect.y1 + .5)
            outside = [s['text'] for s in spans if not bounds.contains(fitz.Rect(s['bbox']))]
            check(tag + '-text-bounds', 'pass' if not outside else 'fail', outside)
        images = []
        for info in page.get_image_info():
            a, b, c, d, _, _ = info['transform']
            width_in, height_in = math.hypot(a, b) / 72, math.hypot(c, d) / 72
            if width_in and height_in:
                images.append(round(min(info['width'] / width_in, info['height'] / height_in), 2))
        row['image_effective_ppi'] = images
        if args.min_ppi:
            check(tag + '-image-ppi', 'pass' if not images or min(images) >= args.min_ppi else 'fail',
                  {'minimum_requested': args.min_ppi, 'placed_images': images,
                   'note': 'No raster images' if not images else 'Inspect source history for upsampling'})
        if args.render_dir or decoder:
            pixels = (page.rect.width * args.dpi / 72) * (page.rect.height * args.dpi / 72)
            if pixels > 40_000_000:
                check(tag + '-render', 'unavailable', 'Render exceeds 40 megapixels; lower --dpi.')
                continue
            pix = page.get_pixmap(dpi=round(args.dpi), colorspace=fitz.csRGB, alpha=False)
            if args.render_dir:
                output = args.render_dir / f'{args.pdf.stem}-page-{index + 1}.png'
                pix.save(output)
                row['render'] = str(output.resolve())
            if decoder:
                image_module, barcode_module = decoder
                im = image_module.frombytes('RGB', [pix.width, pix.height], pix.samples)
                found = {x.text for x in barcode_module.read_barcodes(im)
                         if x.format == barcode_module.BarcodeFormat.QRCode}
                row['qr_payloads'] = sorted(found)
                payloads.update(found)
    combined = '\n'.join(all_text)
    for required in args.require_text:
        check('required-text', 'pass' if required in combined else 'fail', required)
    if decoder:
        expected = set(args.qr)
        check('qr-payloads', 'pass' if payloads == expected else 'fail',
              {'expected_unique': sorted(expected), 'decoded_unique': sorted(payloads),
               'dpi': round(args.dpi)})
    doc.close()
    return finish()


if __name__ == '__main__':
    sys.exit(main())
