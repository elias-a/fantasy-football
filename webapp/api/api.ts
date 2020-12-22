import Router from 'koa-router';
import { controller, Controller } from './controller';

export class Api {
    router: Router;
    controller: Controller;

    constructor(controller: Controller) {
        this.router = new Router({
            prefix: '/api'
        });
        this.controller = controller;
    }
}

export const api = new Api(controller);