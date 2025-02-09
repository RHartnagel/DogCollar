'use strict';

console.log("🚀 Initializing Sequelize and Database Connection...");

const fs = require('fs');
const path = require('path');
const Sequelize = require('sequelize');
const process = require('process');
const basename = path.basename(__filename);
const env = process.env.NODE_ENV || 'development';
const config = require(__dirname + '/../config/config.json')[env];

const db = {};

let sequelize;

if (process.env.DATABASE_URL) {
  sequelize = new Sequelize(process.env.DATABASE_URL, {
    dialect: 'postgres',
    logging: false,
  });
} else {
  sequelize = new Sequelize(config.database, config.username, config.password, config);
}

// Authenticate the database connection
sequelize.authenticate()
  .then(() => console.log("✅ Database connection successful"))
  .catch((err) => console.error("❌ Database connection failed:", err));

// Import models dynamically
fs.readdirSync(__dirname)
  .filter((file) => {
    return (
      file.indexOf('.') !== 0 &&
      file !== basename &&
      file.slice(-3) === '.js' &&
      file.indexOf('.test.js') === -1
    );
  })
  .forEach((file) => {
    const model = require(path.join(__dirname, file))(sequelize, Sequelize.DataTypes);
    db[model.name] = model;
  });

// Run model associations
Object.keys(db).forEach((modelName) => {
  if (db[modelName].associate) {
    db[modelName].associate(db);
  }
});

db.sequelize = sequelize;
db.Sequelize = Sequelize;

// Sync database structure with existing PostgreSQL tables
sequelize.sync({ alter: true }) // Matches Sequelize models with the existing database
  .then(() => console.log('✅ Sequelize models are synced with the database'))
  .catch((err) => console.error('❌ Sync error:', err));

module.exports = db;
