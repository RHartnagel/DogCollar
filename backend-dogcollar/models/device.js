'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  const Device = sequelize.define(
    "Device",
    {
      deviceID: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      userID: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
      deviceName: {
        type: DataTypes.STRING,
        allowNull: false,
      },
    },
    { timestamps: false }
  );

  Device.associate = (models) => {
    Device.belongsTo(models.User, { foreignKey: "userID", onDelete: "CASCADE" });
  };

  return Device;
};
