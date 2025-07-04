'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function AuthClient() {
    const router = useRouter()

    useEffect(() => {
        const cekAuth = async () => {
            try {
                const res = await fetch('/api/user', {
                    method: 'GET',
                })

                if (res.status === 401) {
                    router.replace('/login') // Jika token expired
                }
            } catch (err) {
                console.error("Error checking auth:", err)
                router.replace('/login') // fallback kalau error
            }
        }

        cekAuth()
    }, [])

    return null // tidak perlu render apa-apa
}
