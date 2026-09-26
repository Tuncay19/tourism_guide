const { PrismaClient } = require("@prisma/client");

// Bütün tətbiq boyu tək Prisma instansı istifadə olunur
const prisma = new PrismaClient();

module.exports = prisma;
