import { Create, SimpleForm } from 'react-admin';

export const GenericCreate = ({ fields }) => (
  <Create>
    <SimpleForm>
      {fields.map((field) => {
        const Component = field.component;
        // Передаём все пропсы, включая choices, type и т.д.
        const props = {
          source: field.name,
          label: field.label,
          choices: field.choices,
          type: field.type,
          ...field.props,
        };
        return <Component key={field.name} {...props} />;
      })}
    </SimpleForm>
  </Create>
);