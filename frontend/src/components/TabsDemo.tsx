/**
 * 🎯 DEMONSTRAÇÃO DAS ABAS
 * Componente para demonstrar as abas organizadas por plataforma
 */

import React from "react";

const TabsDemo: React.FC = () => {
  return (
    <div className='bg-white rounded-lg shadow-lg p-6 mb-6'>
      <h3 className='text-lg font-bold text-gray-800 mb-4'>
        ✨ Sistema de Abas por Plataforma
      </h3>

      <div className='grid md:grid-cols-3 gap-4 text-sm'>
        <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
          <div className='flex items-center gap-2 mb-2'>
            <span className='text-xl'>🎓</span>
            <span className='font-semibold text-blue-800'>Google Scholar</span>
          </div>
          <p className='text-blue-700'>
            Publicações acadêmicas, citações, h-index e métricas de impacto
          </p>
        </div>

        <div className='bg-green-50 border border-green-200 rounded-lg p-4'>
          <div className='flex items-center gap-2 mb-2'>
            <span className='text-xl'>🇧🇷</span>
            <span className='font-semibold text-green-800'>
              Plataforma Lattes
            </span>
          </div>
          <p className='text-green-700'>
            Currículos acadêmicos brasileiros, formação e experiência
            profissional
          </p>
        </div>

        <div className='bg-purple-50 border border-purple-200 rounded-lg p-4'>
          <div className='flex items-center gap-2 mb-2'>
            <span className='text-xl'>🌐</span>
            <span className='font-semibold text-purple-800'>ORCID</span>
          </div>
          <p className='text-purple-700'>
            Identificador internacional de pesquisador e produções científicas
          </p>
        </div>
      </div>

      <div className='mt-4 p-4 bg-gray-50 rounded-lg'>
        <h4 className='font-semibold text-gray-800 mb-2'>💡 Como funciona:</h4>
        <ul className='text-sm text-gray-600 space-y-1'>
          <li>
            • <strong>Busca completa:</strong> Solicitar 10 resultados = 10 de
            cada plataforma (total: 30)
          </li>
          <li>
            • <strong>Abas organizadas:</strong> Visualize resultados separados
            por plataforma
          </li>
          <li>
            • <strong>Links diretos:</strong> Clique nos resultados para acessar
            a fonte original
          </li>
          <li>
            • <strong>Contadores:</strong> Veja quantos resultados foram
            encontrados em cada plataforma
          </li>
        </ul>
      </div>
    </div>
  );
};

export default TabsDemo;
