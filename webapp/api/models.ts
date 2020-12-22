import { Sequelize, DataTypes } from 'sequelize';

export class Models {
    sequelize: Sequelize;

    constructor(sequelize: Sequelize) {
        this.sequelize = sequelize;

        if (!this.sequelize.authenticate()) {
            console.log("Failed to connect to database");
        }
    }
}

export const models = new Models(new Sequelize({
    dialect: 'sqlite',
    storage: 'data.db',
    query: {
        raw: true
    },
    logging: false
}));