# 仅为代码学习

## Run

### 1. Granting `execution` permissions to scripts

```bash
chmod  -R +x ./scripts
chmod  -R +x ./tests
chmod  +x Dockerfile
chmod  +x docker-compose.yml
```

### 2. Build and run

```bash
./scripts/build_and_run.sh
```

The above commands will successfully run the entire project with **good network** environment.

Also,you can first **build** the project and then **run** it.

```bash
./scripts/build.sh
./scripts/run_and_restart.sh
```
### 3. Test

```bash
./tests/sdcs-test.sh 3
```


### 3. Stop the project

```bash
./scripts/stop.sh
```

### 4. Restart the project

```bash
./scripts/run_and_restart.sh
```


