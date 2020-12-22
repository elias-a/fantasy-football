import Router from 'koa-router';
import path from 'path';
import { createReadStream } from 'fs';
import { models, Models } from './models';

export class Routes {
    router: Router;

    constructor(models: Models) {
        this.router = new Router();

        this.router.get('/login', async (ctx) => {
            ctx.type = 'html';
            ctx.body = createReadStream(path.join(__dirname, '../web/index.html'));
        });

        this.router.get('/dashboard', async (ctx) => {
            ctx.redirect('/');
        });
    }
}

export const routes = new Routes(models);