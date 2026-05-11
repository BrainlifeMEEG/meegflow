# Configuration Reference

Pipelines are defined in YAML. The top-level key is `pipeline`, which is a list of step objects. Each step has a `name` field plus any parameters that step accepts.

## Minimal example

```yaml
pipeline:
  - name: bandpass_filter
    l_freq: 0.5
    h_freq: 40.0
  - name: epoch
    tmin: -0.2
    tmax: 0.8
  - name: save_clean_instance
```

## Available steps

### Data loading / setup

| Step | Key parameters |
|------|---------------|
| `set_montage` | `montage` (str), `match_case` (bool) |
| `drop_unused_channels` | `channels` (list) |
| `strip_recording` | `tmin`, `tmax` |
| `copy_instance` | `source`, `dest` |
| `concatenate_recordings` | `instances` (list) |

### Filtering

| Step | Key parameters |
|------|---------------|
| `bandpass_filter` | `l_freq`, `h_freq`, `picks`, `n_jobs` |
| `notch_filter` | `freqs` (list), `picks`, `n_jobs` |
| `resample` | `sfreq`, `npad`, `n_jobs`, `resample_events` |

### Referencing

| Step | Key parameters |
|------|---------------|
| `reference` | `ref_channels` (default `'average'`), `instance` |

### Bad channel detection

| Step | Key parameters |
|------|---------------|
| `find_flat_channels` | `threshold` (default `1e-12`), `picks`, `excluded_channels` |
| `find_bads_channels_threshold` | `reject` (dict), `n_epochs_bad_ch`, `picks`, `apply_on` |
| `find_bads_channels_variance` | `zscore_thresh`, `max_iter`, `picks`, `instance`, `apply_on` |
| `find_bads_channels_high_frequency` | `zscore_thresh`, `max_iter`, `picks`, `instance`, `apply_on` |

### Bad channel handling

| Step | Key parameters |
|------|---------------|
| `interpolate_bad_channels` | `instance`, `picks` |
| `drop_bad_channels` | `instance` |

### ICA

| Step | Key parameters |
|------|---------------|
| `ica` | `n_components`, `method`, `fit_params`, `picks`, `eog_channel`, `ecg_channel` |

### Epoching

| Step | Key parameters |
|------|---------------|
| `find_events` | `get_events_from` (`'annotations'`\|`'stim_channel'`), `shortest_event`, `event_id`, `stim_channel` |
| `epoch` | `event_id`, `tmin`, `tmax`, `baseline`, `reject` |
| `chunk_in_epoch` | `duration` |
| `find_bads_epochs_threshold` | `reject` (dict), `n_channels_bad_epoch`, `picks` |

### Output

| Step | Key parameters |
|------|---------------|
| `save_clean_instance` | `instance` (`'raw'`\|`'epochs'`), `overwrite` |
| `generate_json_report` | *(no parameters)* |
| `generate_html_report` | `picks`, `excluded_channels`, `outlines`, `compare_instances` |

## Common parameter patterns

### `picks`

Accepts any value that MNE's `pick_types` understands (e.g. `'eeg'`, `['eeg', 'meg']`, or a list of channel names).

### `excluded_channels`

A list of channel names to exclude from the step (e.g. reference electrodes).

### `apply_on`

Some bad-channel detection steps accept `apply_on: [raw, epochs]` to mark the found bad channels on multiple instances simultaneously.

### `instance`

Steps that can act on either raw or epoched data accept an `instance` key: `'raw'` or `'epochs'`.
