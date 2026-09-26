const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const FacebookStrategy = require("passport-facebook").Strategy;
const prisma = require("../utils/prismaClient");

// Bir provider vasitəsilə giriş edən istifadəçini tapır, yoxdursa yaradır
async function findOrCreateOAuthUser({ provider, providerAccountId, email, fullName, avatarUrl }) {
  // 1) Bu provider ilə əvvəllər qeydiyyatdan keçib?
  const existingAccount = await prisma.account.findUnique({
    where: { provider_providerAccountId: { provider, providerAccountId } },
    include: { user: true },
  });

  if (existingAccount) {
    return existingAccount.user;
  }

  // 2) Eyni email ilə LOCAL və ya başqa provider-dən hesab varmı? Varsa ona bağla
  let user = email ? await prisma.user.findUnique({ where: { email } }) : null;

  if (!user) {
    user = await prisma.user.create({
      data: {
        email: email || `${provider.toLowerCase()}_${providerAccountId}@no-email.qarabagtour.com`,
        fullName: fullName || "İstifadəçi",
        avatarUrl,
        isVerified: true,
      },
    });
  }

  await prisma.account.create({
    data: { userId: user.id, provider, providerAccountId },
  });

  return user;
}

passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: process.env.GOOGLE_CALLBACK_URL,
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        const user = await findOrCreateOAuthUser({
          provider: "GOOGLE",
          providerAccountId: profile.id,
          email: profile.emails?.[0]?.value,
          fullName: profile.displayName,
          avatarUrl: profile.photos?.[0]?.value,
        });
        done(null, user);
      } catch (err) {
        done(err, null);
      }
    }
  )
);

passport.use(
  new FacebookStrategy(
    {
      clientID: process.env.FACEBOOK_CLIENT_ID,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET,
      callbackURL: process.env.FACEBOOK_CALLBACK_URL,
      profileFields: ["id", "displayName", "emails", "photos"],
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        const user = await findOrCreateOAuthUser({
          provider: "FACEBOOK",
          providerAccountId: profile.id,
          email: profile.emails?.[0]?.value,
          fullName: profile.displayName,
          avatarUrl: profile.photos?.[0]?.value,
        });
        done(null, user);
      } catch (err) {
        done(err, null);
      }
    }
  )
);

// Session-a yalnız user ID yazılır (JWT istifadə etdiyimiz üçün minimal saxlanılır)
passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => {
  try {
    const user = await prisma.user.findUnique({ where: { id } });
    done(null, user);
  } catch (err) {
    done(err, null);
  }
});

module.exports = passport;
