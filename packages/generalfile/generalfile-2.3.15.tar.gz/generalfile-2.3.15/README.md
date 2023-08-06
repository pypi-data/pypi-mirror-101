# generalfile
Easily manage files cross platform.

This package and 3 other make up [ManderaGeneral](https://github.com/Mandera).

## Information
| Package                                                      | Ver                                             | Latest Release        | Python                                                                                                                   | Platform        |   Lvl | Todo                                                     | Tests   |
|:-------------------------------------------------------------|:------------------------------------------------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|------:|:---------------------------------------------------------|:--------|
| [generalfile](https://github.com/ManderaGeneral/generalfile) | [2.3.15](https://pypi.org/project/generalfile/) | 2021-04-10 14:44 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu |     1 | [11](https://github.com/ManderaGeneral/generalfile#Todo) | 95.5 %  |

## Contents
<pre>
<a href='#generalfile'>generalfile</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                                | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/send2trash'>send2trash</a>   | <a href='https://pypi.org/project/appdirs'>appdirs</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   |
|:---------------------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------|:---------------------------------------------------------|:-------------------------------------------------------|
| `pip install generalfile`              | Yes                                                                    | Yes                                                            | Yes                                                      | No                                                     |
| `pip install generalfile[spreadsheet]` | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |
| `pip install generalfile[full]`        | Yes                                                                    | Yes                                                            | Yes                                                      | Yes                                                    |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/__init__.py#L1'>Module: generalfile</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/errors.py#L6'>Class: CaseSensitivityError</a>
├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/errors.py#L10'>Class: InvalidCharacterError</a>
└─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path.py#L17'>Class: Path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L32'>Method: absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_lock.py#L124'>Method: as_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/optional_dependencies/path_cfg.py#L12'>Property: cfg</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L477'>Method: contains</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L157'>Method: copy</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L218'>Method: copy_to_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L288'>Method: create_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L362'>Method: delete</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L395'>Method: delete_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L267'>Method: empty</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L267'>Method: encode</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L93'>Method: endswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L259'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L24'>Method: from_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L334'>Method: get_cache_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L451'>Method: get_differing_files</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L344'>Method: get_lock_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L353'>Method: get_lock_path</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L306'>Method: get_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L59'>Method: is_absolute</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L234'>Method: is_file</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L240'>Method: is_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L433'>Method: is_identical</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L66'>Method: is_relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L246'>Method: is_root</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_lock.py#L115'>Method: lock</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L260'>Method: match</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L73'>Method: mirror_path</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L226'>Method: move</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L152'>Method: name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L298'>Method: open_folder</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L97'>Method: open_operation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L497'>Method: pack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L144'>Method: parts</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L118'>Method: read</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L42'>Method: relative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L119'>Method: remove_end</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L102'>Method: remove_start</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L133'>Method: rename</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L135'>Method: same_destination</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path.py#L105'>Method: scrub</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L412'>Method: seconds_since_creation</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L420'>Method: seconds_since_modified</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L325'>Method: set_working_dir</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L427'>Method: size</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/optional_dependencies/path_spreadsheet.py#L9'>Property: spreadsheet</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L84'>Method: startswith</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L168'>Method: stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L200'>Method: suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L244'>Method: suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/optional_dependencies/path_text.py#L11'>Property: text</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L16'>Method: to_alternative</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L384'>Method: trash</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L404'>Method: trash_folder_content</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L184'>Method: true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L516'>Method: unpack</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L159'>Method: with_name</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L175'>Method: with_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L208'>Method: with_suffix</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L251'>Method: with_suffixes</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_strings.py#L191'>Method: with_true_stem</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L279'>Method: without_file</a>
   └─ <a href='https://github.com/ManderaGeneral/generalfile/blob/f651bb2/generalfile/path_operations.py#L106'>Method: write</a>
</pre>

## Todo
| Module                                                                                                                                               | Message                                                                                                                                                                                     |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_operations.py#L1'>path_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_operations.py#L364'>Proper decorator to optionally suppress specified errors.</a>                       |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L1'>decorators.py</a>                                   | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L1'>Tests for decorators, not sure why they aren't found for readme.</a>                       |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L1'>decorators.py</a>                                   | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/decorators.py#L2'>Warn for redundant requirements. (Both file and lib requires pandas.)</a>                  |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L22'>Add a proper place for all variables, add working_dir, sys.executable and sys.prefix to it.</a> |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L23'>Raise suppressable warning if space in Path.</a>                                                |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L24'>Binary extension.</a>                                                                           |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_lock.py#L1'>path_lock.py</a>                                     | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_lock.py#L12'>Actually lock the additional paths given to Path.lock()</a>                                |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L1'>path_spreadsheet.py</a> | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/optional_dependencies/path_spreadsheet.py#L113'>Support DataFrame and Series with spreadsheet.append()</a>   |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_operations.py#L1'>path_operations.py</a>                         | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_operations.py#L477'>Create unittest for 'contains'.</a>                                                 |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_strings.py#L1'>path_strings.py</a>                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path_strings.py#L73'>Create unittest for 'mirror_path'.</a>                                                  |
| <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L1'>path.py</a>                                               | <a href='https://github.com/ManderaGeneral/generalfile/blob/master/generalfile/path.py#L105'>Create unittest for 'scrub'.</a>                                                               |

<sup>
Generated 2021-04-10 14:44 CEST for commit <a href='https://github.com/ManderaGeneral/generalfile/commit/f651bb2'>f651bb2</a>.
</sup>
