# Bug Triage AI Agent - Vercel Deployment Guide

This guide provides step-by-step instructions for deploying the Bug Triage AI Agent backend on Vercel.

## Important Notes

⚠️ **Vercel Limitations:**
- Vercel runs applications as **serverless functions** (not long-running processes)
- Each request may experience a **cold start** delay (1-3 seconds)
- MongoDB connections need to be handled carefully in serverless environments
- Function execution time limit: 10 seconds (Hobby), 60 seconds (Pro)
- Memory limit: 1024 MB (Hobby), 3008 MB (Pro)

✅ **Best For:**
- Low to medium traffic applications
- API endpoints that can handle cold starts
- Cost-effective serverless deployment

❌ **Not Ideal For:**
- High-traffic applications requiring instant responses
- Long-running processes
- Applications requiring persistent connections

---

## Prerequisites

- A GitHub account with the repository containing the Bug Triage AI Agent code
- A Vercel account (sign up at [vercel.com](https://vercel.com))
- MongoDB database (MongoDB Atlas recommended for serverless)

---

## Step-by-Step Deployment

### Step 1: Prepare MongoDB for Serverless

**Important:** For Vercel serverless functions, use MongoDB Atlas (recommended) or ensure your MongoDB supports connection pooling.

1. **MongoDB Atlas Setup:**
   - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster (M0)
   - Configure network access:
     - Add IP: `0.0.0.0/0` (allow all IPs) OR
     - Add Vercel IP ranges (check Vercel documentation for current ranges)
   - Create database user
   - Get connection string (SRV format recommended)
   - Connection string format: `mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority`

2. **Connection String Parameters for Serverless:**
   - Add `retryWrites=true&w=majority` to connection string
   - Consider adding `maxPoolSize=10` for connection pooling
   - Example: `mongodb+srv://user:pass@cluster.mongodb.net/db?retryWrites=true&w=majority&maxPoolSize=10`

### Step 2: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

Or use the web interface (no CLI needed).

### Step 3: Deploy via Vercel Dashboard

#### Option A: Import from GitHub

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New...** → **Project**
3. Import your GitHub repository:
   - Select: `The-Ahmad-Behzad/bug-triage-agent`
   - Click **Import**

4. **Configure Project:**
   - **Framework Preset:** Other (or leave as auto-detected)
   - **Root Directory:** `bug-triage-agent` ⚠️ **Important: Set this!**
   - **Build Command:** Leave empty (Vercel auto-detects Python)
   - **Output Directory:** Leave empty
   - **Install Command:** Leave empty

5. **Environment Variables:**
   Click **Environment Variables** and add:
   - **Key:** `MONGODB_URI`
     - **Value:** Your MongoDB Atlas connection string
     - **Environments:** Production, Preview, Development (select all)
   
   - **Key:** `MONGODB_DB_NAME`
     - **Value:** `bug_triage_agent`
     - **Environments:** Production, Preview, Development (select all)

6. **Deploy:**
   - Click **Deploy**
   - Wait for deployment to complete (2-5 minutes)

#### Option B: Deploy via CLI

1. **Login to Vercel:**
   ```bash
   cd bug-triage-agent
   vercel login
   ```

2. **Deploy:**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project? No (first time)
   - Project name: `bug-triage-agent`
   - Directory: `./` (current directory)
   - Override settings? No

3. **Set Environment Variables:**
   ```bash
   vercel env add MONGODB_URI
   # Paste your MongoDB connection string when prompted
   # Select: Production, Preview, Development
   
   vercel env add MONGODB_DB_NAME
   # Enter: bug_triage_agent
   # Select: Production, Preview, Development
   ```

4. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Step 4: Verify Deployment

1. **Check Deployment Status:**
   - Go to Vercel Dashboard → Your Project
   - Check the deployment logs for any errors

2. **Test Endpoints:**
   ```bash
   # Health check
   curl https://your-project.vercel.app/health
   
   # Root endpoint
   curl https://your-project.vercel.app/
   
   # API docs
   # Visit: https://your-project.vercel.app/docs
   ```

3. **Expected Response (Health Check):**
   ```json
   {
     "status": "healthy",
     "agent_name": "bug_triage_agent",
     "version": "1.0.0",
     "timestamp": "2025-01-XX...",
     "details": {
       "database": "connected",
       ...
     }
   }
   ```

---

## Project Structure for Vercel

```
bug-triage-agent/
├── api/
│   └── index.py          # Vercel serverless handler
├── src/                   # Application source code
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── ...
```

---

## Configuration Files

### vercel.json

The `vercel.json` file configures:
- Build settings
- Routing rules
- Environment variables
- Python path

**Current Configuration:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

### api/index.py

This file wraps the FastAPI application with Mangum to make it compatible with Vercel's serverless environment.

---

## Troubleshooting

### Issue: Cold Start Delays

**Symptoms:** First request after inactivity takes 2-5 seconds

**Solutions:**
- This is normal for serverless functions
- Consider using Vercel Pro plan for better performance
- Implement request warming (ping endpoint periodically)
- Use MongoDB connection pooling (already configured)

### Issue: MongoDB Connection Errors

**Symptoms:** `ServerSelectionTimeoutError` or connection failures

**Solutions:**
1. **Check MongoDB Atlas Network Access:**
   - Ensure `0.0.0.0/0` is allowed OR
   - Add Vercel IP ranges

2. **Verify Connection String:**
   - Use SRV format: `mongodb+srv://...`
   - Include `retryWrites=true&w=majority`
   - Check username/password are correct

3. **Check Environment Variables:**
   - Verify `MONGODB_URI` is set in Vercel dashboard
   - Ensure it's set for all environments (Production, Preview, Development)

4. **Connection Pooling:**
   - MongoDB Atlas handles this automatically
   - For self-hosted MongoDB, ensure connection pooling is enabled

### Issue: Function Timeout

**Symptoms:** Request fails after 10 seconds (Hobby plan) or 60 seconds (Pro)

**Solutions:**
- Optimize database queries
- Reduce processing time in handlers
- Consider upgrading to Pro plan for 60-second limit
- Break long operations into smaller functions

### Issue: Import Errors

**Symptoms:** `ModuleNotFoundError` or import failures

**Solutions:**
1. **Check PYTHONPATH:**
   - `vercel.json` sets `PYTHONPATH: "."`
   - Ensure this is correct

2. **Verify File Structure:**
   - Ensure `api/index.py` exists
   - Check that `src/` directory is included in deployment

3. **Check Dependencies:**
   - Verify all packages are in `requirements.txt`
   - Check deployment logs for missing packages

### Issue: 404 Errors on Routes

**Symptoms:** All routes return 404

**Solutions:**
- Verify `vercel.json` routing configuration
- Check that `api/index.py` exports the handler correctly
- Ensure FastAPI app is properly wrapped with Mangum

### Issue: CORS Errors

**Symptoms:** Browser shows CORS errors when calling API

**Solutions:**
- CORS is configured in `src/main/app.py`
- Currently allows all origins (`*`)
- For production, restrict to specific domains:
  ```python
  allow_origins=["https://your-frontend.vercel.app"]
  ```

---

## Performance Optimization

### 1. Connection Pooling

MongoDB Atlas automatically handles connection pooling. The application uses singleton pattern for connections, which works well with serverless.

### 2. Cold Start Mitigation

- **Keep Functions Warm:** Use external service (e.g., UptimeRobot) to ping `/health` every 5 minutes
- **Upgrade Plan:** Pro plan has better cold start performance
- **Optimize Imports:** Lazy load heavy modules when possible

### 3. Database Optimization

- Use MongoDB Atlas indexes for faster queries
- Implement caching for frequently accessed data
- Optimize database queries to reduce execution time

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MONGODB_URI` | Yes | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db?retryWrites=true&w=majority` |
| `MONGODB_DB_NAME` | No | Database name (default: `bug_triage_agent`) | `bug_triage_agent` |

---

## Vercel Plans Comparison

| Feature | Hobby (Free) | Pro ($20/month) |
|---------|--------------|-----------------|
| Function Execution Time | 10 seconds | 60 seconds |
| Memory | 1024 MB | 3008 MB |
| Bandwidth | 100 GB | 1 TB |
| Cold Start Performance | Standard | Optimized |
| Team Collaboration | ❌ | ✅ |

---

## Alternative: Render.com

If Vercel's serverless limitations are problematic, consider using **Render.com** instead:
- Long-running processes (no cold starts)
- Better for high-traffic applications
- See `DEPLOYMENT.md` for Render.com instructions

---

## Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Mangum Documentation](https://mangum.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)

---

## Deployment Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] Network access configured (allow Vercel IPs or `0.0.0.0/0`)
- [ ] Database user created
- [ ] Connection string obtained
- [ ] Vercel account created
- [ ] GitHub repository connected to Vercel
- [ ] Root directory set to `bug-triage-agent`
- [ ] Environment variables configured (`MONGODB_URI`, `MONGODB_DB_NAME`)
- [ ] Deployment successful
- [ ] Health endpoint tested: `https://your-project.vercel.app/health`
- [ ] API documentation accessible: `https://your-project.vercel.app/docs`
- [ ] Test execute endpoint with sample request

---

## Support

For issues:
- **Vercel:** Check [Vercel Status](https://www.vercel-status.com/) or [Vercel Support](https://vercel.com/support)
- **MongoDB:** Refer to [MongoDB Atlas Support](https://www.mongodb.com/support)
- **Application:** Check deployment logs in Vercel Dashboard

