import { spawnSync } from 'child_process';
import { models, Models } from './models';

export class Controller {
    models: Models;

    constructor(models: Models) {
        this.models = models;
    }

    async getTeamData() {
        const teams = await this.getTeams();
        const managers = await this.getManagers();

        return {
            teams,
            managers
        }
    }

    async getTeams() {
        const py = spawnSync('python3', ['../main.py', 'teams']);
        return JSON.parse(py.stdout.toString());
    }

    async getManagers() {
        const py = spawnSync('python3', ['../main.py', 'managers']);
        return JSON.parse(py.stdout.toString());
    }
}

export const controller = new Controller(models);