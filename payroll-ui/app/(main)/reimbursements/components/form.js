import {toast} from "react-hot-toast";
import {useEffect, useState} from "react";
import dayjs from 'dayjs';

import {Datepicker} from 'flowbite-react';

export default function ReimbursementForm({onSubmit, onClose, initialData = {}, reimbursement = null}) {
    const [loading, setLoading] = useState(false);
    const [claimDate, setClaimDate] = useState(new Date());
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData(event.target);
        let data = Object.fromEntries(formData.entries());
        data.claim_date = dayjs(claimDate).format("YYYY-MM-DD");
        let url = `/api/reimbursements`
        if (reimbursement) {
            url += `/${reimbursement.id}`;
        }
        const response = await fetch(url, {
            method: reimbursement ? 'PUT' :     'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (response.ok) {
            toast.success(reimbursement ? 'Reimbursements edit failed' : 'Reimbursements created failed');
            onSubmit();
            setLoading(false);
            return;
        }
        toast.error(reimbursement ? 'Reimbursements edit failed' : 'Reimbursements created failed');
        setLoading(false);
    }
    useEffect(() => {
        if (reimbursement) {
            setClaimDate(new Date(reimbursement.claim_date));
            document.getElementById('amount').value = reimbursement.amount || '';
            document.getElementById('description').value = reimbursement.description || '';
        } else {
            setClaimDate(new Date());
        }
    }, [reimbursement])
    return (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="relative p-4 w-full max-w-2xl max-h-full">
                <div className="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
                    <form onSubmit={handleSubmit}>
                        <div
                            className="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600 border-gray-200">
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                                {reimbursement ? 'Edit Reimbursement' : 'Create Reimbursement'}
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
                                <label htmlFor="amount"
                                       className="block mb-2 text-sm font-bold text-gray-900 dark:text-white">Claim
                                    Date</label>
                                <div className="relative max-w-sm">
                                    <div
                                        className="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                                        <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                             xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                            <path
                                                d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"/>
                                        </svg>
                                    </div>
                                    <Datepicker value={claimDate} onChange={(val) => setClaimDate(val)}/>
                                </div>
                                <div>
                                    <label htmlFor="amount"
                                           className="block mb-2 text-sm font-bold text-gray-900 dark:text-white">Amount</label>
                                    <input
                                        type="number"
                                        name="amount"
                                        id="amount"
                                        defaultValue={initialData.amount || ''}
                                        required
                                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-400 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="description"
                                           className="block mb-2 text-sm font-bold text-gray-900 dark:text-white">Description</label>
                                    <textarea
                                        name="description"
                                        id="description"
                                        defaultValue={initialData.description || ''}
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