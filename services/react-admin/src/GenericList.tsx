import { List, Datagrid, TextField, NumberField, BooleanField, EditButton, DeleteButton, ShowButton } from 'react-admin';

// Карта компонентов для разных типов полей
const fieldComponents = {
    text: TextField,
    number: NumberField,
    boolean: BooleanField,
};

export const GenericList = ({ fields, resource }) => (
    <List>
        <Datagrid>
            {fields.map((field) => {
                const Component = fieldComponents[field.type] || TextField;
                return <Component key={field.name} source={field.name} label={field.label} />;
            })}
            <ShowButton />
            <EditButton />
            <DeleteButton />
        </Datagrid>
    </List>
);