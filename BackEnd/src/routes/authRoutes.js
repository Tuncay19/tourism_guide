const express = require("express");
const passport = require("passport");
const { signup, login, getMe, oauthSuccess } = require("../controllers/authController");
const { requireAuth } = require("../middleware/auth");

const router = express.Router();

// ---- Email + şifrə ----
router.post("/signup", signup);
router.post("/login", login);
router.get("/me", requireAuth, getMe);

// ---- Google OAuth ----
router.get("/google", passport.authenticate("google", { scope: ["profile", "email"] }));
router.get(
  "/google/callback",
  passport.authenticate("google", { session: false, failureRedirect: "/login-failed" }),
  oauthSuccess
);

// ---- Facebook OAuth ----
router.get("/facebook", passport.authenticate("facebook", { scope: ["email"] }));
router.get(
  "/facebook/callback",
  passport.authenticate("facebook", { session: false, failureRedirect: "/login-failed" }),
  oauthSuccess
);

module.exports = router;
