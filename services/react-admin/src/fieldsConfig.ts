import { TextInput, NumberInput, BooleanInput, SelectInput } from 'react-admin';

export const fieldsConfig = {
    tariffs: [
        { name: 'id', label: 'ID', type: 'number' },
        { name: 'ship_from', label: 'Откуда', type: 'text' },
        { name: 'ship_to', label: 'Куда', type: 'text' },
        { name: 'cargo_type', label: 'Тип груза', type: 'text' },
        { name: 'price', label: 'Цена', type: 'number' },
        { name: 'delivery_days_min', label: 'Мин. дней', type: 'number' },
        { name: 'delivery_days_max', label: 'Макс. дней', type: 'number' },
        { name: 'is_active', label: 'Активен', type: 'boolean' },
        { name: 'delivery_type', label: 'Тип доставки', type: 'text' },
    ],
    carriers: [
        { name: 'id', label: 'ID', type: 'number' },
        { name: 'name', label: 'Название', type: 'text' },
        { name: 'rating', label: 'Рейтинг', type: 'number' },
        // добавьте другие поля
    ],
    users: [
        { name: 'id', label: 'ID', type: 'number' },
        { name: 'username', label: 'Логин', type: 'text' },
        { name: 'email', label: 'Email', type: 'text' },
        { name: 'first_name', label: 'Имя', type: 'text' },
        { name: 'last_name', label: 'Фамилия', type: 'text' },
        { name: 'phone', label: 'Телефон', type: 'text' },
        { name: 'is_staff', label: 'Админ', type: 'boolean' },
        { name: 'role', label: 'Роль', type: 'text' },
    ],
    orders: [
        // добавьте поля заказа
    ],
};