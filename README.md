# FindingRecordedFile

A Python script to search and extract recorded files from Kubernetes pods using user-defined parameters like date, pod type, file type, and search string. Designed for flexible environments where file structure, naming, and pod layout may vary.

---

## ✅ Features

- Search for specific files across Kubernetes pods using:
  - Content matching (string search)
  - File name patterns
  - Optional date filtering
- Supports multiple pod deployments automatically
- Copies matching files locally or to a custom path
- Zips and optionally transfers files using `sz` (optional)

---

## 🧩 Input Parameters (Interactive)

- **Date** (optional): `YYYYMMDD` format; leave blank to use today's data or inspect temporary directories.
- **File Type**: e.g. `sms`, `rec`, `data`, or custom keyword for file filtering.
- **Service Selection**:
  ```
  0 → onlinecharging
  1 → convergedcharging
  2 → bizmngcharging
  3 → rerating
  4 → recurringrating
  ```
- **Mode**: `pps` or `pos`
- **Search String**: A value to find within files (e.g. phone number, ID)
- **Save Location**: Optional local directory to store matching files (`/tmp/recorded_file/` by default)
- **Temp Only**: Choose whether to search only in `temp/` folders
- **Fail Mode**: Toggle between `normal` or `fail` file structures

---

## 📁 Folder Layout

Default search path is built as:

```
/onip/recorded_file/<service>/output/<pps|pos>/<normal|fail>[/temp]
```

If a date is provided, it looks under backup folders:

```
/onip/recorded_file/.../backup/filecleanerbak/<YYYYMMDD>/
```

> All paths can be customized by editing the script.

---

## ⚙️ Kubernetes Interaction

- Uses `kubectl get pod`, `kubectl exec`, and `kubectl cp` to:
  - Detect active pods by name
  - Execute search commands
  - Copy matched files from pods to local disk
- Namespace is configurable (default is `namespace`)

---

## 🗂 Output

- Matched files are copied to:
  - `/tmp/recorded_file/` (default), or
  - User-specified folder
- Files are compressed into a zip (`*.zip`)
- Optionally downloaded using `sz` (requires `sz` to be installed)

---

## 🚀 Run the Script

```bash
python Kubern_Search.py
```

Follow the prompts to input your values interactively.

---

## 🧰 Requirements

- Python 3.x
- `kubectl` with configured access
- `sz` (optional, for file transfer) (need download rpm file)
- Read access to files inside pods

---

## 📝 Notes

- File types, pod service names, and paths are fully customizable inside the script.
- Designed for manual, interactive use but can be automated.
- Supports both normal and backup file locations.
- This code Need modification based on your pods name , file path and file name.

---

## 📄 License

Internal or private use. Modify and use freely.
