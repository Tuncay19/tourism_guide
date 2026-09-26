require("dotenv").config();
const express = require("express");
const cors = require("cors");
const session = require("express-session");
const passport = require("./config/passport");
const authRoutes = require("./routes/authRoutes");

const app = express();

app.use(cors({ origin: process.env.CLIENT_URL, credentials: true }));
app.use(express.json());

// Passport OAuth axını üçün session lazımdır (özü login vəziyyətini saxlamır, JWT istifadə olunur)
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
  })
);
app.use(passport.initialize());
app.use(passport.session());

// ---- Route-lar ----
app.use("/api/auth", authRoutes);

app.get("/", (req, res) => {
  res.json({ message: "Qarabağ Tur Platforması API işləyir 🇦🇿" });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server ${PORT} portunda işə düşdü`);
});
