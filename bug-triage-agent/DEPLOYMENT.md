# Bug Triage AI Agent - Render.com Deployment Guide

This guide provides step-by-step instructions for deploying the Bug Triage AI Agent backend on Render.com with GitHub integration.

## Prerequisites

Before deploying, ensure you have:

- A GitHub account with the repository containing the Bug Triage AI Agent code
- A Render.com account (sign up at [render.com](https://render.com))
- MongoDB database (Render managed or external like MongoDB Atlas)

## Deployment Options

You can deploy using either:
1. **Render Blueprint (Infrastructure as Code)** - Recommended for automated setup
2. **Manual Configuration** - Step-by-step setup via Render Dashboard

---

## Option 1: Deploy Using Render Blueprint (Recommended)

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to GitHub
2. Verify that `render.yaml` exists in the `bug-triage-agent/` directory
3. Ensure all dependencies are listed in `requirements.txt`

### Step 2: Create MongoDB Service (if using Render managed)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **MongoDB**
3. Configure:
   - **Name**: `bug-triage-mongodb` (or your preferred name)
   - **Plan**: Select appropriate plan (Starter is fine for development)
   - **Region**: Choose closest to your web service
4. Click **Create Database**
5. Wait for the database to be provisioned
6. Copy the **Internal Connection String** (you'll need this in Step 3)

### Step 3: Deploy Web Service from Blueprint

1. In Render Dashboard, click **New +** → **Blueprint**
2. Connect your GitHub repository
3. Select the branch (typically `main` or `master`)
4. Render will detect `render.yaml` and show the services to be created
5. Before creating, you'll need to set the `MONGODB_URI` environment variable:
   - If using Render managed MongoDB: Use the **Internal Connection String** from Step 2
   - If using external MongoDB: Use your external connection string (e.g., MongoDB Atlas)
6. Review the configuration and click **Apply**
7. Render will create the service and start the first deployment

### Step 4: Verify Deployment

1. Wait for the deployment to complete (check the Events tab)
2. Visit your service URL: `https://your-service-name.onrender.com`
3. Test the health endpoint: `https://your-service-name.onrender.com/health`
4. Check API documentation: `https://your-service-name.onrender.com/docs`

---

## Option 2: Manual Configuration via Dashboard

### Step 1: Create MongoDB Service (if using Render managed)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **MongoDB**
3. Configure:
   - **Name**: `bug-triage-mongodb`
   - **Plan**: Select appropriate plan
   - **Region**: Choose closest region
4. Click **Create Database**
5. Wait for provisioning and copy the **Internal Connection String**

### Step 2: Create Web Service

1. In Render Dashboard, click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `bug-triage-agent`
   - **Region**: Same as MongoDB (if using Render managed)
   - **Branch**: `main` or `master`
   - **Root Directory**: `bug-triage-agent`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main.app:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

1. In your service settings, go to **Environment** section
2. Add the following environment variables:
   - **MONGODB_URI**: 
     - If using Render managed MongoDB: Paste the Internal Connection String
     - If using external MongoDB: Paste your external connection string
   - **MONGODB_DB_NAME**: `bug_triage_agent` (optional, this is the default)

### Step 4: Configure Health Check

1. In service settings, scroll to **Health Check Path**
2. Set to: `/health`
3. This enables Render to monitor your service health

### Step 5: Enable Auto-Deploy

1. In service settings, go to **Auto-Deploy** section
2. Select **On Commit** to enable automatic deploys on push/merge
3. Alternatively, select **After CI Checks Pass** if you have CI/CD pipelines

### Step 6: Deploy

1. Click **Create Web Service**
2. Render will start the first deployment
3. Monitor the deployment in the **Events** tab
4. Wait for deployment to complete

### Step 7: Verify Deployment

1. Check service logs for any errors
2. Visit: `https://your-service-name.onrender.com/health`
3. Verify the health check returns `"status": "healthy"` or `"status": "degraded"` (degraded is OK if MongoDB isn't connected yet)
4. Test API docs: `https://your-service-name.onrender.com/docs`

---

## MongoDB Setup Options

### Option A: Render Managed MongoDB (Recommended for Simplicity)

**Pros:**
- Easy setup and management
- Automatic backups
- Internal networking (faster, more secure)
- Integrated with Render dashboard

**Steps:**
1. Create MongoDB service in Render Dashboard
2. Use the **Internal Connection String** provided
3. Set as `MONGODB_URI` environment variable in your web service

**Connection String Format:**
```
mongodb://[username]:[password]@[host]:[port]/[database]?[options]
```

### Option B: MongoDB Atlas (External)

**Pros:**
- Free tier available
- Global distribution
- Advanced features

**Steps:**
1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Configure network access (add Render IPs or allow all)
4. Create database user
5. Get connection string
6. Set as `MONGODB_URI` environment variable

**Network Access:**
- For Render services, you may need to allow all IPs (`0.0.0.0/0`) or add specific Render IP ranges
- Check MongoDB Atlas documentation for current Render IP ranges

### Option C: Other External MongoDB

- Use any MongoDB-compatible service
- Ensure network access is configured
- Set connection string as `MONGODB_URI`

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGODB_URI` | Yes | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGODB_DB_NAME` | No | `bug_triage_agent` | Database name |
| `PORT` | No | `8000` | Server port (automatically set by Render) |

---

## Post-Deployment Verification

### 1. Health Check

```bash
curl https://your-service-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent_name": "bug_triage_agent",
  "version": "1.0.0",
  "timestamp": "2025-01-XX...",
  "details": {
    "database": "connected",
    "uptime_seconds": 123,
    "totals": {...}
  }
}
```

### 2. API Documentation

Visit: `https://your-service-name.onrender.com/docs`

You should see the Swagger UI with all available endpoints.

### 3. Test Execute Endpoint

```bash
curl -X POST https://your-service-name.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test-001",
    "sender": "supervisor",
    "bugs": [...]
  }'
```

### 4. Check Logs

- Go to Render Dashboard → Your Service → **Logs** tab
- Verify no errors during startup
- Check database connection messages

---

## Troubleshooting

### Issue: Deployment Fails During Build

**Symptoms:** Build command fails, service doesn't start

**Solutions:**
- Check that `requirements.txt` is in the `bug-triage-agent/` directory
- Verify Python version compatibility (requires Python 3.11+)
- Check build logs for specific package installation errors
- Ensure all dependencies are listed in `requirements.txt`

### Issue: Service Starts But Health Check Fails

**Symptoms:** Service is running but `/health` returns 500 or times out

**Solutions:**
- Check service logs for application errors
- Verify MongoDB connection string is correct
- Ensure MongoDB is accessible from Render (network configuration)
- Check that `MONGODB_URI` environment variable is set correctly

### Issue: Database Connection Errors

**Symptoms:** Health check shows `"database": "disconnected"`

**Solutions:**
- Verify `MONGODB_URI` is set correctly in environment variables
- For Render managed MongoDB: Use Internal Connection String (not External)
- For external MongoDB: Ensure network access allows Render IPs
- Check MongoDB service is running and accessible
- Verify database credentials are correct

### Issue: Port Already in Use

**Symptoms:** Service fails to start with port error

**Solutions:**
- This shouldn't happen on Render (PORT is automatically set)
- If using custom start command, ensure it uses `$PORT` not hardcoded port
- Verify start command: `uvicorn src.main.app:app --host 0.0.0.0 --port $PORT`

### Issue: Auto-Deploy Not Working

**Symptoms:** Changes pushed to GitHub don't trigger deployment

**Solutions:**
- Check Auto-Deploy is enabled in service settings
- Verify correct branch is linked
- Check if commit message contains `[skip render]` or `[render skip]`
- Manually trigger deploy: **Manual Deploy** → **Deploy latest commit**

### Issue: Service Goes to Sleep (Free Tier)

**Symptoms:** Service is slow to respond after inactivity

**Solutions:**
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes longer (cold start)
- Consider upgrading to paid plan for always-on service
- Use external monitoring service to ping `/health` periodically

---

## Configuration Best Practices

### Production Recommendations

1. **CORS Configuration**: Update `src/main/app.py` to restrict CORS origins instead of allowing all (`*`)

2. **Environment Variables**: Use Render's environment variable management for sensitive data

3. **Database**: Use Render managed MongoDB for better integration, or MongoDB Atlas for production workloads

4. **Monitoring**: Set up external monitoring (e.g., UptimeRobot) to ping `/health` endpoint

5. **Logging**: Monitor logs regularly via Render Dashboard

6. **Backups**: Ensure MongoDB backups are configured (automatic with Render managed MongoDB)

---

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Deploy Guide](https://render.com/docs/deploys)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

## Support

For issues specific to:
- **Render Platform**: Check [Render Status](https://status.render.com) or [Render Support](https://render.com/docs/support)
- **Application Code**: Check application logs in Render Dashboard
- **MongoDB**: Refer to MongoDB documentation or support channels

---

## Deployment Checklist

- [ ] GitHub repository is connected to Render
- [ ] MongoDB service is created and running
- [ ] `MONGODB_URI` environment variable is set
- [ ] `MONGODB_DB_NAME` is set (if different from default)
- [ ] Root directory is set to `bug-triage-agent`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn src.main.app:app --host 0.0.0.0 --port $PORT`
- [ ] Health check path: `/health`
- [ ] Auto-deploy is enabled (if desired)
- [ ] Health endpoint returns successful response
- [ ] API documentation is accessible at `/docs`
- [ ] Test execute endpoint with sample request

