'use client';
import {toast} from "react-hot-toast";
import {useEffect, useState} from "react";

export default function Attendances() {
    const [attendanceData, setAttendanceData] = useState([]);
    const [currentAttendanceData, setCurrentAttendanceData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingCurrent, setLoadingCurrent] = useState(false);
    const fetchAttendances = async () => {
        setLoading(true);
        const response = await fetch('/api/attendance', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        });
        if (!response.ok) {
            toast.error('Failed to fetch attendances');
            setLoading(false);
            return;
        }
        const data = await response.json();
        setAttendanceData(data);
        setLoading(false);
    };
    const fetchCurrentAttendance = async () => {
        setLoadingCurrent(true);
        const response = await fetch('/api/attendance/current', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        });
        if (!response.ok) {
            toast.error('Failed to fetch get current attendances');
            setLoadingCurrent(false);
            return
        }
        const results = await response.json();
        setCurrentAttendanceData(results.data);
        setLoadingCurrent(false);
    };

    const handleClockInOut = async () => {
        setLoadingCurrent(true);
        const response = await fetch('/api/attendance/clock', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
            }
        });
        if (!response.ok) {
            toast.error('Failed to clock in/out');
            setLoadingCurrent(false);
            return;
        }
        toast.success(currentAttendanceData ? 'Clocked out successfully' : 'Clocked in successfully');
        await fetchCurrentAttendance();
        await fetchAttendances();
        setLoadingCurrent(false);
    }
    useEffect(() => {
        fetchCurrentAttendance();
        fetchAttendances();
    }, [])
    return (
        <div className="flex flex-col justify-start min-h-screen">
            <h1 className="text-4xl font-bold mb-4">Attendances</h1>
            <div className="flex flex-col space-y-4 sm:flex-row justify-start sm:space-y-0 mb-4 gap-2">
                {!currentAttendanceData?.clock_out && (
                    <button
                        disabled={loadingCurrent}
                        onClick={handleClockInOut}
                        className="cursor-pointer px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        {loadingCurrent ? 'Fetching data..' : currentAttendanceData ? 'Clock Out' : 'Clock In'}
                    </button>
                )}

                {currentAttendanceData && (
                    <div className="flex items-center gap-2 py-2 font-medium">
                        <span>{currentAttendanceData.clock_date_display} :</span>
                        <span>Clock In: {currentAttendanceData.clock_in_display}</span>
                        {currentAttendanceData.clock_out_display && (
                            <>
                                <span>-</span>
                                <span>Clock Out: {currentAttendanceData.clock_out_display}</span>
                                <span className="font-bold">(Duration: {currentAttendanceData.duration_display})</span>
                            </>
                        )}
                    </div>
                )}
            </div>
            <div className="relative overflow-x-auto">
                {loading ? 'fetching data attendances...' : (
                    <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                        <thead
                            className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" className="px-6 py-3">
                                Clock Date
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Clock Out
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Clock In
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Duration
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        {attendanceData.map((attendance, index) => (
                            <tr key={index}
                                className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                                <th scope="row"
                                    className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                    {attendance.clock_date_display || 'N/A'}
                                </th>
                                <td className="px-6 py-4">
                                    {attendance.clock_in_display || 'N/A'}
                                </td>
                                <td className="px-6 py-4">
                                    {attendance.clock_out_display || 'N/A'}
                                </td>
                                <td className="px-6 py-4 font-bold text-gray-900 whitespace-nowrap dark:text-white">
                                    {attendance.duration_display}
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                )}
            </div>

        </div>
    )
}