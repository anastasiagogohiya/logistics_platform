import { Admin, Resource, EditGuesser, ShowGuesser } from 'react-admin';
import { authProvider } from './authProvider';
import { dataProvider } from './dataProvider';
import Dashboard from './Dashboard';
import { GenericCreate } from './GenericCreate';
import { GenericList } from './GenericList';
import { fieldsConfig } from './fieldsConfig';

const App = () => (
  <Admin
    dashboard={Dashboard}
    authProvider={authProvider}
    dataProvider={dataProvider}
    title="Logistics Admin"
  >
    <Resource
      name="users"
      list={<GenericList fields={fieldsConfig.users} resource="users" />}
      create={<GenericCreate fields={fieldsConfig.users} />}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="orders"
      list={<GenericList fields={fieldsConfig.orders} resource="orders" />}
      create={<GenericCreate fields={fieldsConfig.orders} />}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="tariffs"
      list={<GenericList fields={fieldsConfig.tariffs} resource="tariffs" />}
      create={<GenericCreate fields={fieldsConfig.tariffs} />}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="carriers"
      list={<GenericList fields={fieldsConfig.carriers} resource="carriers" />}
      create={<GenericCreate fields={fieldsConfig.carriers} />}
      edit={EditGuesser}
      show={ShowGuesser}
    />
  </Admin>
);

export default App;