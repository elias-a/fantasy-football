import { Sequelize, DataTypes } from 'sequelize';
import { db, user, password } from './config';

export class Models {
    sequelize: Sequelize;
    Player: any;

    constructor(sequelize: Sequelize) {
        this.sequelize = sequelize;

        if (!this.sequelize.authenticate()) {
            console.log("Failed to connect to database");
        }

        this.init();
    }

    async init() {
        await this.initPlayer();
    }

    async initPlayer() {
        this.Player = this.sequelize.define('Player', {
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true
            },
            name: {
                type: DataTypes.STRING
            },
            passYards: {
                type: DataTypes.FLOAT
            },
            passTouchdowns: {
                type: DataTypes.FLOAT
            },
            interceptions: {
                type: DataTypes.FLOAT
            },
            rushYards: {
                type: DataTypes.FLOAT
            },
            rushTouchdowns: {
                type: DataTypes.FLOAT
            },
            receptions: {
                type: DataTypes.FLOAT
            },
            receivingYards: {
                type: DataTypes.FLOAT
            },
            receivingTouchdowns: {
                type: DataTypes.FLOAT
            },
            points: {
                type: DataTypes.FLOAT
            }
        }, {
            tableName: 'Player',
            timestamps: false
        });

        await this.Player.sync();
    }
}

export const models = new Models(new Sequelize(db, user, password, {
    dialect: 'postgres',
    query: {
        raw: true
    },
    logging: false
}));