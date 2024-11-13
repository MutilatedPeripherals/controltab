# controltab

## Backend setup

```bash
cd diffing
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Start the server

```bash
fastapi dev main.py
```

## Frontend setup

```bash
cd visualizer
npm install
npm run dev
```

TODOs:
* when we accept a change, then also save the history of the previous version.
* when we have the history available in the db, then provide a rollback functionality.
* what do we do with dangling files. we should have a scheduler which checks that any file not being a part of a history gets deleted or sth.
* changes in different instruments
* figure out how to merge the two Visualizer components. do we show alphatabs per change or do we highlight the changes in one alphatab?