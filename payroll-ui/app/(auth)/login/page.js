'use client';
import Card from "@/components/card";
import {useState} from "react";
import {toast} from "react-hot-toast";
import Cookies from "js-cookie";
import {useRouter} from "next/navigation";

export default function Home() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [email, setState] = useState("");
    const [password, setPassword] = useState("");
    const handleError = async (response) => {
        setLoading(false);
        const errorData = await response.json();
        if (errorData instanceof Object) {
            for (const [key, value] of Object.entries(errorData)) {
                if (Array.isArray(value)) {
                    for (let j = 0; j < value.length; j++) {
                        toast.error(`${key}: ${value[j]}`);
                    }
                } else {
                    toast.error(`${key}: ${value}`);
                }
            }
        } else {
            toast.error(`Login failed: ${errorData.message || 'Unknown error'}`);
        }
        return false;
    }
    const handleLogin = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("email", email);
        formData.append("password", password);

        setLoading(true);
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            return await handleError(response);
        }

        const data = await response.json();
        Cookies.set('auth_token', data.token);

        const responseUser = await fetch('/api/user', {method: 'GET',
            headers: {
                'Accept': 'application/json',
                // 'Authorization': `Bearer ${Cookies.get('auth_token') || ''}`,
            }
        });
        if (!responseUser.ok) {
            return await handleError(responseUser);
        }
        toast.success("Login successful");
        const dataUser = await responseUser.json();
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user', JSON.stringify(dataUser));
        setLoading(false);
        router.replace('/dashboard');
    }
    return (
        <div
            className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
            <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
                <Card title="Login to Payroll App"
                      description="Please enter your credentials to access the payroll system.">
                    <form className="max-w-sm mx-auto" onSubmit={handleLogin}>
                        <div className="mb-5">
                            <label htmlFor="email"
                                   className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email
                                Address</label>
                            <input type="email" id="email"
                                   className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                   value={email}
                                   onChange={e => setState(e.target.value)}
                                   placeholder="name@example.com" required/>
                        </div>
                        <div className="mb-5">
                            <label htmlFor="password"
                                   className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                            <input type="password" id="password"
                                   className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                   value={password}
                                   onChange={e => setPassword(e.target.value)}
                                   required/>
                        </div>
                        <button type="submit"
                                className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                                disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>
                </Card>
            </main>
        </div>
    );
}
