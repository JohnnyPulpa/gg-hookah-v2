import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './contexts/LanguageContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import DrinksQuestion from './pages/DrinksQuestion';
import DrinksCatalog from './pages/DrinksCatalog';
import Checkout from './pages/Checkout';
import Orders from './pages/Orders';

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="catalog" element={<Catalog />} />
            <Route path="drinks-question" element={<DrinksQuestion />} />
            <Route path="drinks" element={<DrinksCatalog />} />
            <Route path="checkout" element={<Checkout />} />
            <Route path="orders" element={<Orders />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
