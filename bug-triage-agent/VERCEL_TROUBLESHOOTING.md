# Vercel Deployment Troubleshooting

## Common Issues and Solutions

### Issue: FUNCTION_INVOCATION_FAILED / 500 Error

**Symptoms:**
- Serverless function crashes on deployment
- Error: `FUNCTION_INVOCATION_FAILED`
- Code: `500: INTERNAL_SERVER_ERROR`

**Root Causes & Solutions:**

#### 1. Startup Tasks Running at Import Time

**Problem:** The original code ran `startup_tasks()` at module import, which tried to connect to MongoDB immediately. In serverless, this can crash the function.

**Solution:** ✅ Fixed - Startup tasks now run lazily on first request.

#### 2. MongoDB Connection Failing

**Problem:** MongoDB connection attempts at import time can fail and crash the function.

**Solution:** ✅ Fixed - MongoDB connection is now lazy and handles errors gracefully.

**Additional Checks:**
- Verify `MONGODB_URI` environment variable is set in Vercel
- Check MongoDB Atlas network access allows `0.0.0.0/0` or Vercel IPs
- Ensure connection string format is correct (SRV format recommended)

#### 3. Import Path Issues

**Problem:** Python can't find modules due to path issues.

**Solution:** ✅ Fixed - Added proper path setup in `api/index.py`

**If still having issues:**
- Check that `PYTHONPATH` is set to `.` in `vercel.json`
- Verify all files are committed to git
- Check deployment logs for specific import errors

#### 4. Missing Dependencies

**Problem:** Required packages not installed.

**Solution:**
- Verify `requirements.txt` includes all dependencies
- Check deployment logs for missing package errors
- Ensure `mangum` is in requirements.txt (added for Vercel)

### Issue: Build Command / Output Directory Questions

**Why leave them empty?**

- **Build Command:** Vercel automatically detects Python and runs `pip install -r requirements.txt`
- **Output Directory:** Not needed for Python serverless functions - Vercel serves from the function location
- **Install Command:** Vercel handles dependency installation automatically

**When to specify:**
- Only if you have custom build steps (e.g., compiling assets, running scripts)
- For most Python/FastAPI apps, leaving empty is correct

### Issue: Cold Start Delays

**Symptoms:** First request after inactivity takes 2-5 seconds

**This is normal for serverless!** Solutions:
- Use Vercel Pro plan for better performance
- Keep functions warm (ping `/health` every 5 minutes)
- Optimize imports (lazy load heavy modules)

### Issue: MongoDB Connection Timeouts

**Symptoms:** Database operations fail with timeout errors

**Solutions:**
1. **Check Connection String:**
   - Use MongoDB Atlas SRV format
   - Include `retryWrites=true&w=majority`
   - Add `maxPoolSize=10` for connection pooling

2. **Network Access:**
   - MongoDB Atlas: Allow `0.0.0.0/0` (all IPs)
   - Or add Vercel IP ranges

3. **Connection Settings:**
   - Timeouts are set to 3 seconds (serverless-friendly)
   - Connection pooling is enabled

### Issue: Environment Variables Not Working

**Symptoms:** App can't find `MONGODB_URI` or other env vars

**Solutions:**
1. **Check Vercel Dashboard:**
   - Go to Project → Settings → Environment Variables
   - Verify variables are set for all environments (Production, Preview, Development)

2. **Redeploy After Adding Variables:**
   - Environment variables require a new deployment
   - Click "Redeploy" after adding variables

3. **Check Variable Names:**
   - Must match exactly: `MONGODB_URI`, `MONGODB_DB_NAME`
   - Case-sensitive

### Issue: Routes Return 404

**Symptoms:** All endpoints return 404

**Solutions:**
1. **Check `vercel.json` routing:**
   ```json
   {
     "routes": [
       {
         "src": "/(.*)",
         "dest": "api/index.py"
       }
     ]
   }
   ```

2. **Verify handler export:**
   - `api/index.py` must export `handler`
   - Check that Mangum is wrapping the FastAPI app correctly

3. **Check Root Directory:**
   - Must be set to `bug-triage-agent` in Vercel settings

### Issue: Import Errors in Logs

**Symptoms:** `ModuleNotFoundError` or import failures

**Solutions:**
1. **Check File Structure:**
   ```
   bug-triage-agent/
   ├── api/
   │   └── index.py
   ├── src/
   │   └── ...
   └── requirements.txt
   ```

2. **Verify PYTHONPATH:**
   - `vercel.json` sets `PYTHONPATH: "."`
   - This allows imports like `from src.main.app import app`

3. **Check Dependencies:**
   - All packages must be in `requirements.txt`
   - Vercel installs from requirements.txt automatically

### Debugging Steps

1. **Check Deployment Logs:**
   - Vercel Dashboard → Your Project → Deployments → Click deployment → View Function Logs

2. **Test Locally with Vercel CLI:**
   ```bash
   cd bug-triage-agent
   vercel dev
   ```

3. **Check Environment Variables:**
   ```bash
   vercel env ls
   ```

4. **View Function Logs:**
   ```bash
   vercel logs [deployment-url]
   ```

### Recent Fixes Applied

✅ **Lazy Startup Tasks:** Startup tasks now run on first request, not at import time
✅ **Resilient MongoDB Connection:** Connection errors don't crash the function
✅ **Better Error Handling:** Added try-catch blocks and graceful degradation
✅ **Path Fixes:** Improved Python path handling for serverless

### Still Having Issues?

1. **Check Vercel Status:** https://www.vercel-status.com/
2. **Review Deployment Logs:** Detailed error messages in Vercel Dashboard
3. **Test Health Endpoint:** `https://your-project.vercel.app/health`
4. **Verify MongoDB:** Test connection string separately

### Quick Verification Checklist

- [ ] `MONGODB_URI` environment variable set in Vercel
- [ ] `MONGODB_DB_NAME` environment variable set (optional)
- [ ] Root directory set to `bug-triage-agent`
- [ ] All files committed and pushed to GitHub
- [ ] MongoDB Atlas network access configured
- [ ] Deployment logs checked for specific errors
- [ ] Health endpoint tested: `/health`

