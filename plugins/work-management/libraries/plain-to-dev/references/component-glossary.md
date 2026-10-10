# Component Glossary

Use this file when the user describes what a UI element looks like or does, but does not know its technical name.

## Dialogs and Alerts

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Popup with two buttons | Modal dialog / `<dialog>` / alert dialog | `UIAlertController` (alert) | `AlertDialog` | Confirmation dialog |
| Popup with a list of options | Dropdown / menu / action menu | `UIAlertController` (action sheet) | `AlertDialog` with list | Action sheet / option list |
| Popup that fills most of the screen | Modal / dialog | Presented view controller | `DialogFragment` | Modal |
| Popup you cannot dismiss | Non-dismissible modal | Alert without cancel path | Non-cancelable `AlertDialog` | Blocking dialog |
| Delete confirmation popup | Confirmation dialog | Destructive `UIAlertController` | Destructive `AlertDialog` | Destructive action confirmation |

## Notifications and Feedback

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Quick message that disappears | Snackbar / toast | Toast-like transient message | Snackbar / toast | Snackbar / toast |
| Banner at top of screen | Notification banner | Notification banner | Heads-up notification / banner | In-app banner |
| Red number dot | Notification badge | App icon badge | App badge | Badge / unread indicator |
| Small dot on a button or icon | Badge / chip | Badge overlay | Badge | Notification indicator |

## Navigation

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Top bar with app name and back button | Header / app bar / nav | `UINavigationBar` | `Toolbar` / app bar | Navigation bar |
| Bottom bar with section icons | Bottom nav / tab bar | `UITabBar` / `TabView` | `BottomNavigationView` | Tab bar / bottom navigation |
| Side panel with nav links | Drawer / sidebar | Side menu / split view | `NavigationDrawer` | Navigation drawer |
| Three-line menu icon | Hamburger button | Menu button | Drawer toggle | Hamburger menu |
| Breadcrumb trail | Breadcrumb nav |  |  | Breadcrumb navigation |
| Floating button in corner | FAB |  | `FloatingActionButton` | Floating action button |

## Overlays and Sheets

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Panel that slides up from bottom | Bottom sheet / slide-up panel | `UISheetPresentationController` | `BottomSheetDialog` | Bottom sheet |
| Panel that slides in from side | Drawer / side sheet | Side panel | Side sheet | Drawer / side sheet |
| Darkened background behind popup | Backdrop / overlay / scrim | Dim overlay | Scrim | Modal scrim / backdrop |
| Hover explanation | Tooltip | Tooltip | Tooltip | Tooltip |
| Small popup near a button | Popover | `UIPopoverPresentationController` | `PopupWindow` / popup menu | Popover |

## Forms and Inputs

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Text box | `<input type="text">` | `UITextField` / `TextField` | `EditText` / text field | Text input |
| Bigger text area | `<textarea>` | `UITextView` | Multiline `EditText` | Textarea |
| Pick one from a menu | `<select>` / dropdown | `UIPickerView` | Spinner / dropdown menu | Select / dropdown |
| On/off switch | Toggle / styled checkbox | `UISwitch` / `Toggle` | `Switch` | Toggle / switch |
| Several checkboxes | Checkbox group | Checkbox list | Checkbox list | Multi-select |
| One choice from several | Radio group | Radio list | `RadioGroup` | Single-select |
| Range slider | `<input type="range">` | `UISlider` | `Slider` | Slider |
| Error under a field | Inline validation / field error | Error label | `TextInputLayout` error | Inline field validation |
| Step-by-step form | Multi-step form / wizard | Step flow | Stepper | Wizard / stepper |
| Search bar | `<input type="search">` | `UISearchBar` | `SearchBar` | Search input |
| Date picker | Date input / date picker | `UIDatePicker` | `MaterialDatePicker` | Date picker |

## Lists and Grids

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Scrolling list of items | List / `role=\"list\"` | `UITableView` / `List` | `RecyclerView` / `LazyColumn` | List view |
| Grid of cards or images | CSS grid / flex grid | `UICollectionView` / `LazyVGrid` | Grid `RecyclerView` | Grid view |
| Loads more as you scroll | Infinite scroll / virtual scroll | Paginated list | Paginated `RecyclerView` | Infinite scroll |
| Grouped list with headers | Grouped list | Grouped table view | Sectioned list | Grouped list |
| Swipeable image slideshow | Carousel / image slider | `UIPageViewController` | `ViewPager2` / pager | Carousel |
| Draggable sortable list | Drag-and-drop list | Move rows | Drag-and-drop list | Sortable list |

## Loading and State

| Plain description | Web | iOS | Android | General pattern |
| --- | --- | --- | --- | --- |
| Spinning loading circle | Spinner / `role=\"progressbar\"` | `UIActivityIndicatorView` | `CircularProgressIndicator` | Loading spinner |
| Progress bar | `<progress>` | `UIProgressView` | `LinearProgressIndicator` | Progress bar |
| Gray placeholder while loading | Skeleton screen / shimmer | Skeleton / shimmer | Shimmer | Skeleton loading |
| Placeholder when nothing exists yet | Empty state / zero state | Empty state view | Empty state | Zero state |
| Pull down to refresh | Pull-to-refresh | `UIRefreshControl` | `SwipeRefreshLayout` | Refresh control |

## Ambiguity Flags

These inputs usually need clarification before naming the term:
- `popup`
- `notification`
- `menu`
- `overlay`
- `banner`
- `card`
- `form`
- `list`

Clarify in this order:
1. platform
2. whether it blocks the rest of the screen
3. what triggers it
4. what content appears inside it

## Output Hint

When answering from this file, give:
- the pattern name
- the platform-specific term if relevant
- what a developer would search for

If the user is no longer asking for a name and is really describing a feature, switch to `idea-to-spec.md`.
