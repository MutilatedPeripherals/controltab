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