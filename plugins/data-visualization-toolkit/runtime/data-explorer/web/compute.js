export function compute(data,view){
  const rows=data.rows.filter(row=>{
    const v=row.values;
    if(view.category_column!==null&&v[view.category_column]!==view.category_value)return false;
    const f=view.numeric_filter;if(!f)return true;
    const n=v[f.column];if(n===null)return f.include_missing;
    return (f.min===null||n>=f.min)&&(f.max===null||n<=f.max);
  });
  const col=view.sort.column,dir=view.sort.direction==='desc'?-1:1;
  rows.sort((a,b)=>{const av=col==='id'?a.id:a.values[col],bv=col==='id'?b.id:b.values[col];if(av===null||bv===null)return av===bv?(a.id>b.id?1:a.id<b.id?-1:0):av===null?1:-1;return dir*(av>bv?1:av<bv?-1:0)||(a.id>b.id?1:a.id<b.id?-1:0)});
  const nums=rows.map(r=>r.values[view.measure]).filter(v=>v!==null);
  const known=nums.length,visible=new Set(rows.map(r=>r.id));
  return {rows,aggregate:{row_count:rows.length,known_count:known,missing_count:rows.length-known,min:known?Math.min(...nums):null,max:known?Math.max(...nums):null,mean:known?nums.reduce((m,x,i)=>m+x/(i+1)-m/(i+1),0):null,denominator:known,selected_ids:view.selected_ids,selected_visible_ids:rows.filter(r=>view.selected_ids.includes(r.id)).map(r=>r.id),selected_hidden_ids:view.selected_ids.filter(id=>!visible.has(id))}};
}
export function defaultView(data){return {category_column:null,category_value:null,numeric_filter:null,measure:data.columns.find(c=>c.type==='number').key,sort:{column:'id',direction:'asc'},selected_ids:[]}}
