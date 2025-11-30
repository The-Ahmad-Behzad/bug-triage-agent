# Vercel Deployment - Quick Start

## Prerequisites Checklist

- [ ] MongoDB Atlas account (free tier available)
- [ ] Vercel account (free tier available)
- [ ] GitHub repository: `The-Ahmad-Behzad/bug-triage-agent`

## Quick Deployment Steps

### 1. Setup MongoDB Atlas (5 minutes)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster (M0)
3. **Network Access:** Add IP `0.0.0.0/0` (allow all)
4. **Database Access:** Create user, save password
5. **Connect:** Get connection string (SRV format)
6. Format: `mongodb+srv://username:password@cluster.mongodb.net/db?retryWrites=true&w=majority`

### 2. Deploy to Vercel (5 minutes)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. **Add New** → **Project**
3. Import: `The-Ahmad-Behzad/bug-triage-agent`
4. **Configure:**
   - Root Directory: `bug-triage-agent` ⚠️ **IMPORTANT**
   - Framework: Other (auto-detect)
5. **Environment Variables:**
   - `MONGODB_URI` = Your MongoDB Atlas connection string
   - `MONGODB_DB_NAME` = `bug_triage_agent`
6. Click **Deploy**

### 3. Verify (2 minutes)

1. Wait for deployment (2-5 minutes)
2. Test: `https://your-project.vercel.app/health`
3. Docs: `https://your-project.vercel.app/docs`

## Common Issues

**404 Errors?** → Check Root Directory is set to `bug-triage-agent`

**MongoDB Connection Failed?** → Check network access allows `0.0.0.0/0`

**Cold Start Slow?** → Normal for serverless, first request takes 2-5 seconds

## Full Documentation

See `VERCEL_DEPLOYMENT.md` for detailed instructions and troubleshooting.

