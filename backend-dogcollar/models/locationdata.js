'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  const LocationData = sequelize.define(
    "LocationData",
    {
      locationID: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      deviceID: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
      timestamp: {
        type: DataTypes.DATE,
        allowNull: false,
      },
      latitude: {
        type: DataTypes.DECIMAL(9, 6),
        allowNull: false,
      },
      longitude: {
        type: DataTypes.DECIMAL(9, 6),
        allowNull: false,
      },
    },
    { timestamps: false }
  );

  LocationData.associate = (models) => {
    LocationData.belongsTo(models.Device, { foreignKey: "deviceID", onDelete: "CASCADE" });
  };

  return LocationData;
};
