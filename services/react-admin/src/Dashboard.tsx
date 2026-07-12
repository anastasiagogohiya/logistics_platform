import { Card, CardContent, CardHeader } from '@mui/material';
import { useDataProvider } from 'react-admin';
import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
    const dataProvider = useDataProvider();
    const [stats, setStats] = useState({ tariffs: 0, carriers: 0, users: 0, orders: 0 });

    useEffect(() => {
        dataProvider.getList('tariffs', { pagination: { page: 1, perPage: 1 } })
            .then(res => setStats(prev => ({ ...prev, tariffs: res.total })));
        dataProvider.getList('carriers', { pagination: { page: 1, perPage: 1 } })
            .then(res => setStats(prev => ({ ...prev, carriers: res.total })));
        dataProvider.getList('users', { pagination: { page: 1, perPage: 1 } })
            .then(res => setStats(prev => ({ ...prev, users: res.total })));
        dataProvider.getList('orders', { pagination: { page: 1, perPage: 1 } })
            .then(res => setStats(prev => ({ ...prev, orders: res.total })));
    }, []);

    const data = [
        { name: 'Тарифы', value: stats.tariffs },
        { name: 'Перевозчики', value: stats.carriers },
        { name: 'Пользователи', value: stats.users },
        { name: 'Заказы', value: stats.orders },
    ];

    return (
        <Card>
            <CardHeader title="Статистика" />
            <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={data}>
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="value" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    );
};

export default Dashboard;