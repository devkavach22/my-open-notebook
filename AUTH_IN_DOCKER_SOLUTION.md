# Authentication in Docker - Solution Guide

## The Problem

You're getting 404 errors when trying to access `/api/auth/login` because:

1. **Docker Hub Image**: The `lfnovo/open_notebook:v1-latest` image from Docker Hub doesn't have the authentication code
2. **Local Code**: Your authentication code only exists in your local files
3. **Mismatch**: Docker is running old backend code without auth endpoints

## The Solution

Build a custom Docker image using your local code (which includes auth).

### Step 1: Stop Current Docker Containers

Double-click: `stop-docker.bat`

### Step 2: Rebuild Docker with Your Code

Double-click: `rebuild-docker.bat`

This will:
- Stop existing containers
- Build a new Docker image from your local code (includes auth)
- Start the containers with the new image
- Takes 5-10 minutes to build

### Step 3: Test Authentication

After rebuild completes, test the auth endpoint:

```bash
curl http://localhost:5055/api/auth/status
```

Should return:
```json
{
  "auth_enabled": true,
  "auth_required": true,
  "signup_enabled": true,
  "password_reset_enabled": true,
  "email_verification_enabled": false,
  "oauth_providers": []
}
```

### Step 4: Access Your App

- **Frontend**: http://localhost:8502
- **Backend API**: http://localhost:5055
- **Database**: http://localhost:8000

## What Changed

### docker-compose.yml

**Before:**
```yaml
open_notebook:
  image: lfnovo/open_notebook:v1-latest  # Pull from Docker Hub
  pull_policy: always
```

**After:**
```yaml
open_notebook:
  build:
    context: .
    dockerfile: Dockerfile  # Build from local code
```

## Future Updates

Whenever you make code changes:

1. Stop Docker: `stop-docker.bat`
2. Rebuild: `rebuild-docker.bat`
3. Your changes will be included in the new image

## Alternative: Run Locally (No Docker for Backend)

If you don't want to rebuild Docker every time:

1. Keep database in Docker: `start-database.bat`
2. Run backend locally: `start-backend.bat`
3. Run frontend locally: `start-frontend.bat`

This way you can edit code and see changes immediately without rebuilding Docker.

## Troubleshooting

### Build Fails

If Docker build fails:
- Check Docker Desktop is running
- Check you have enough disk space (needs ~2GB)
- Check internet connection (downloads Node.js and Python packages)

### Still Getting 404

If you still get 404 after rebuild:
1. Check containers are running: `check-docker-status.bat`
2. Check logs: `docker-compose logs open_notebook`
3. Verify auth router is loaded: Look for "auth" in startup logs

### Port Already in Use

If ports 5055 or 8502 are in use:
1. Stop all Docker: `docker-compose down`
2. Stop local processes using those ports
3. Restart: `start-docker.bat`

## Summary

- **Old Way**: Pull pre-built image from Docker Hub (no auth)
- **New Way**: Build image from your local code (has auth)
- **Command**: Double-click `rebuild-docker.bat`
- **Time**: 5-10 minutes first time, faster on subsequent builds
