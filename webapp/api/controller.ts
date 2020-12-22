import { models, Models } from './models';

export class Controller {
    models: Models;

    constructor(models: Models) {
        this.models = models;
    }
}

export const controller = new Controller(models);