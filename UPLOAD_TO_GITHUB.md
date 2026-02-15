# 📤 How to Upload These Files to GitHub

## Step-by-Step Instructions

### **Step 1: Create GitHub Account** (if you don't have one)
1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the steps
4. Verify your email

---

### **Step 2: Create New Repository**

1. **Go to:** [github.com/new](https://github.com/new)
2. **Repository name:** `alpine-backend`
3. **Description:** `Car listing aggregator for OR/WA Craigslist`
4. **Public or Private:** Your choice (both work)
5. **DO NOT** check "Add a README file" (we already have one)
6. Click **"Create repository"**

---

### **Step 3: Upload Files**

You'll see a page with instructions. Look for **"uploading an existing file"** link.

1. Click **"uploading an existing file"**
2. **Drag ALL these files into the browser window:**
   - app.py
   - requirements.txt
   - Procfile
   - runtime.txt
   - railway.json
   - nixpacks.toml
   - README.md
   - .gitignore

3. Scroll down
4. Click **"Commit changes"** (green button)

**✅ Your files are now on GitHub!**

---

### **Step 4: Verify Files Are Uploaded**

You should see all 8 files in your repo:
- ✅ app.py
- ✅ requirements.txt
- ✅ Procfile
- ✅ runtime.txt
- ✅ railway.json
- ✅ nixpacks.toml
- ✅ README.md
- ✅ .gitignore

**IMPORTANT:** Files should be at the ROOT of the repo, NOT inside a folder!

**Good:**
```
alpine-backend/
├── app.py
├── requirements.txt
└── ...
```

**Bad:**
```
alpine-backend/
└── backend/
    ├── app.py
    └── ...
```

---

### **Step 5: Deploy to Railway**

1. **Go to:** [railway.app](https://railway.app)
2. Click **"Login with GitHub"**
3. Authorize Railway
4. Click **"New Project"**
5. Click **"Deploy from GitHub repo"**
6. Select **"alpine-backend"**
7. Railway will:
   - Detect Python
   - Install from requirements.txt
   - Start with Procfile
   - Deploy! ✅

**Wait 2-3 minutes for build to complete.**

---

### **Step 6: Get Your API URL**

1. Click **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. **Copy your URL!**
   - Example: `https://alpine-backend-production.up.railway.app`

---

### **Step 7: Test Your API**

**Visit in browser:**
```
https://your-url.railway.app
```

Should see:
```json
{
  "name": "Alpine Seller Search API",
  "version": "1.0.0",
  "coverage": "All Oregon and Washington Craigslist areas"
}
```

**Test listings:**
```
https://your-url.railway.app/api/listings
```

Should see JSON array of cars!

---

## ✅ Checklist

- [ ] Created GitHub account
- [ ] Created `alpine-backend` repository
- [ ] Uploaded ALL 8 files
- [ ] Files are at ROOT (not in subfolder)
- [ ] Deployed to Railway
- [ ] Generated domain
- [ ] Copied URL
- [ ] Tested `/api/listings` endpoint
- [ ] Saw real car data!

---

## 🐛 Troubleshooting

**"requirements.txt not found":**
- Make sure you uploaded it
- Check it's at the root, not in a folder

**"ModuleNotFoundError":**
- Railway didn't install dependencies
- Go to Settings → Set build command: `pip install -r requirements.txt`
- Redeploy

**"Application Error":**
- Check Railway logs (Deployments → View logs)
- Look for red error messages

---

## 🎯 Next Steps

After backend is deployed:

1. Copy your Railway URL
2. Update `alpine-seller-search-DEPLOY.html` with your URL
3. Upload to Netlify
4. **Your app is LIVE!**

---

**Need help?** Check the Railway logs or create an issue on GitHub!
