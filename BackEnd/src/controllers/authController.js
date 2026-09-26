const bcrypt = require("bcryptjs");
const prisma = require("../utils/prismaClient");
const { generateToken } = require("../utils/jwt");

// POST /api/auth/signup
async function signup(req, res) {
  try {
    const { email, password, fullName } = req.body;

    if (!email || !password || !fullName) {
      return res.status(400).json({ message: "Email, şifrə və ad tələb olunur." });
    }

    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
      return res.status(409).json({ message: "Bu email artıq qeydiyyatdan keçib." });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
      data: { email, password: hashedPassword, fullName },
    });

    const token = generateToken(user);

    return res.status(201).json({
      message: "Qeydiyyat uğurla tamamlandı.",
      token,
      user: sanitizeUser(user),
    });
  } catch (err) {
    console.error("Signup error:", err);
    return res.status(500).json({ message: "Server xətası baş verdi." });
  }
}

// POST /api/auth/login
async function login(req, res) {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "Email və şifrə tələb olunur." });
    }

    const user = await prisma.user.findUnique({ where: { email } });

    if (!user || !user.password) {
      return res.status(401).json({ message: "Email və ya şifrə yanlışdır." });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: "Email və ya şifrə yanlışdır." });
    }

    const token = generateToken(user);

    return res.status(200).json({
      message: "Giriş uğurludur.",
      token,
      user: sanitizeUser(user),
    });
  } catch (err) {
    console.error("Login error:", err);
    return res.status(500).json({ message: "Server xətası baş verdi." });
  }
}

// GET /api/auth/me
async function getMe(req, res) {
  try {
    const user = await prisma.user.findUnique({ where: { id: req.user.userId } });
    if (!user) return res.status(404).json({ message: "İstifadəçi tapılmadı." });
    return res.json({ user: sanitizeUser(user) });
  } catch (err) {
    console.error("GetMe error:", err);
    return res.status(500).json({ message: "Server xətası baş verdi." });
  }
}

// Google/Facebook uğurlu girişindən sonra çağırılır (passport req.user-ə yazır)
function oauthSuccess(req, res) {
  const token = generateToken(req.user);
  // Frontend-ə token ilə birgə yönləndirilir
  const redirectUrl = `${process.env.CLIENT_URL}/oauth-success?token=${token}`;
  return res.redirect(redirectUrl);
}

// Şifrəni cavabdan çıxarmaq üçün köməkçi funksiya
function sanitizeUser(user) {
  const { password, ...safeUser } = user;
  return safeUser;
}

module.exports = { signup, login, getMe, oauthSuccess };
