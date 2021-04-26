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
            position: {
                type: DataTypes.STRING
            },
            season: {
                type: DataTypes.SMALLINT
            },
            passYards: {
                type: DataTypes.REAL
            },
            passTouchdowns: {
                type: DataTypes.REAL
            },
            interceptions: {
                type: DataTypes.REAL
            },
            rushYards: {
                type: DataTypes.REAL
            },
            rushTouchdowns: {
                type: DataTypes.REAL
            },
            receptions: {
                type: DataTypes.REAL
            },
            receivingYards: {
                type: DataTypes.REAL
            },
            receivingTouchdowns: {
                type: DataTypes.REAL
            },
            points: {
                type: DataTypes.REAL
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