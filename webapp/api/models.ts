import { Sequelize, DataTypes } from 'sequelize';

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
                type: DataTypes.NUMBER
            },
            passTouchdowns: {
                type: DataTypes.NUMBER
            },
            interceptions: {
                type: DataTypes.NUMBER
            },
            rushYards: {
                type: DataTypes.NUMBER
            },
            rushTouchdowns: {
                type: DataTypes.NUMBER
            },
            receptions: {
                type: DataTypes.NUMBER
            },
            receivingYards: {
                type: DataTypes.NUMBER
            },
            receivingTouchdowns: {
                type: DataTypes.NUMBER
            },
            points: {
                type: DataTypes.NUMBER
            }
        }, {
            tableName: 'Player',
            timestamps: false
        });

        await this.Player.sync();
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