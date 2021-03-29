import { spawnSync } from 'child_process';
import { models, Models } from './models';

export class Controller {
    models: Models;

    constructor(models: Models) {
        this.models = models;
    }

    async getManagers() {
        const py = spawnSync('python3', ['../main.py']);
        return JSON.parse(py.stdout.toString());
    }
}

export const controller = new Controller(models);