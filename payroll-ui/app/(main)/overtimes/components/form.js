import {toast} from "react-hot-toast";
import {useEffect, useState} from "react";
import dayjs from 'dayjs';

import {Datepicker} from 'flowbite-react';

export default function OvertimeForm({onSubmit, onClose, initialData = {}, item = null}) {
    const [loading, setLoading] = useState(false);
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData(event.target);
        let data = Object.fromEntries(formData.entries());
        let url = `/api/overtimes`
        if (item) {
            url += `/${item.id}`;
        }
        const response = await fetch(url, {
            method: item ? 'PUT' : 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (response.ok) {
            toast.success(item ? 'Overtimes edit failed' : 'Overtimes created failed');
            onSubmit();
            setLoading(false);
            return;
        }
        toast.error(item ? 'Overtimes edit failed' : 'Overtimes created failed');
        setLoading(false);
    }
    useEffect(() => {
        if (item) {
            document.getElementById('hours').value = item.hours || '1';
        }
    }, [item])
    return (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="relative p-4 w-full max-w-2xl max-h-full">
                <div className="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
                    <form onSubmit={handleSubmit}>
                        <div
                            className="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600 border-gray-200">
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                                {item ? 'Edit Overtime' : 'Create Overtime'}
                            </h3>
                            <button
                                onClick={onClose} type="button"
                                className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                                data-modal-hide="default-modal">
                                <svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                                     fill="none" viewBox="0 0 14 14">
                                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                          strokeWidth="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                                </svg>
                                <span className="sr-only">Close modal</span>
                            </button>
                        </div>
                        <div className="p-4 md:p-5 space-y-4">
                            <div className="space-y-6">
                                <div>
                                    <label htmlFor="hours"
                                           className="block mb-2 text-sm font-bold text-gray-900 dark:text-white">Hours</label>
                                    <input
                                        type="number"
                                        name="hours"
                                        id="hours"
                                        max="3"
                                        min="1"
                                        step="any"
                                        defaultValue={initialData.hours || '1'}
                                        required
                                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-400 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                    />
                                </div>
                            </div>
                        </div>
                        <div
                            className="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                            <button disabled={loading} data-modal-hide="default-modal" type="submit"
                                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 cursor-pointer">
                                {loading ? 'Submitting...' : 'Submit'}
                            </button>
                            <button data-modal-hide="default-modal" type="button"
                                    className="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 cursor-pointer"
                                    onClick={onClose}>Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}