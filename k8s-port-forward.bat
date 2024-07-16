@echo off
setlocal

REM This script uses a workaround to get the pod name directly due to service port forwarding issues.
REM For production, use proper ingress in your Kubernetes cluster for secure and efficient exposure.

REM Get the pod name and container port
for /f "tokens=*" %%i in ('kubectl get pods --namespace default -l "app.kubernetes.io/name=voice-bot,app.kubernetes.io/instance=voice-bot" -o jsonpath^="{.items[0].metadata.name}"') do set POD_NAME=%%i
for /f "tokens=*" %%i in ('kubectl get pod --namespace default %POD_NAME% -o jsonpath^="{.spec.containers[0].ports[0].containerPort}"') do set CONTAINER_PORT=%%i

echo Visit http://127.0.0.1:6000 to use your application
echo Setting up port forwarding...
echo Executing command: kubectl --namespace default port-forward %POD_NAME% 6000:%CONTAINER_PORT%
kubectl --namespace default port-forward %POD_NAME% 6000:%CONTAINER_PORT%

REM Script will keep port forwarding active. Press Ctrl+C to stop when done.