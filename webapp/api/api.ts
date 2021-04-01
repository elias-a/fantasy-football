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

        this.router.post('/get-team-data', async (ctx) => {
            const result = await this.controller.getTeamData();
            ctx.status = 200;
            ctx.body = result;
        });
    }
}

export const api = new Api(controller);