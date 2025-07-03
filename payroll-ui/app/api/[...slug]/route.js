import {NextResponse} from "next/server";
import {cookies} from "next/headers";

const BACKEND_API_URL = process.env.BACKEND_API_URL || "http://localhost:8000";

async function forwardRequest(req, pathName) {
    pathName = pathName.replace(/^\/api\//, '/');
    const url = new URL(`${BACKEND_API_URL}/${pathName}/`);
    if (req.method === 'GET' || req.method === 'HEAD') {
        url.search = req.nextUrl.searchParams.toString();
    }

    const cookieStore = await cookies();
    let token = cookieStore.get('auth_token')?.value || '';
    const headers = new Headers(req.headers);
    headers.delete('host');
    headers.delete('cookie');
    headers.delete('authorization');

    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }
    const response = await fetch(url, {
        method: req.method,
        headers: headers,
        body: req.method !== 'GET' && req.method !== 'HEAD' ? await req.text() : null,
    });

    return new NextResponse(response.body, {
        status: response.status,
        headers: response.headers,
    });
}

async function getPath(paramsPromise) {
    const params = await paramsPromise;
    return Array.isArray(params.slug) ? params.slug.join('/') : params.slug;
}

export async function GET(req, { params }) {
    const path = await getPath(params);
    return forwardRequest(req, path);
}

export async function POST(req, { params }) {
    const path = await getPath(params);
    return forwardRequest(req, path);
}

export async function PUT(req, { params }) {
    const path = await getPath(params);
    return forwardRequest(req, path);
}

export async function DELETE(req, { params }) {
    const path = await getPath(params);
    return forwardRequest(req, path);
}