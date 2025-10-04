/**
 * 📊 CARTÕES DE ESTATÍSTICAS
 * Componente para exibir métricas importantes do sistema
 */

import React from "react";
import {
  TrendingUp,
  Users,
  FileText,
  Clock,
  Activity,
  AlertCircle,
} from "lucide-react";

interface StatsData {
  totalSearches: number;
  totalResults: number;
  avgResponseTime: number;
  successRate: number;
  platformsActive: number;
  lastUpdate: string;
}

interface StatsCardsProps {
  stats: StatsData | null;
  isLoading: boolean;
}

const StatsCards: React.FC<StatsCardsProps> = ({ stats, isLoading }) => {
  if (isLoading) {
    return (
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
        {[...Array(6)].map((_, idx) => (
          <div
            key={idx}
            className='bg-white rounded-lg shadow border p-6 animate-pulse'
          >
            <div className='h-4 bg-gray-200 rounded w-1/2 mb-4'></div>
            <div className='h-8 bg-gray-200 rounded w-1/3 mb-2'></div>
            <div className='h-3 bg-gray-200 rounded w-2/3'></div>
          </div>
        ))}
      </div>
    );
  }

  if (!stats) {
    return (
      <div className='bg-red-50 border border-red-200 rounded-lg p-6'>
        <div className='flex items-center'>
          <AlertCircle className='h-5 w-5 text-red-500 mr-2' />
          <p className='text-red-700'>
            Não foi possível carregar as estatísticas do sistema
          </p>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: "Total de Buscas",
      value: stats.totalSearches.toLocaleString("pt-BR"),
      icon: TrendingUp,
      color: "blue",
      description: "Pesquisas realizadas no sistema",
    },
    {
      title: "Resultados Encontrados",
      value: stats.totalResults.toLocaleString("pt-BR"),
      icon: FileText,
      color: "green",
      description: "Total de publicações e perfis",
    },
    {
      title: "Tempo Médio",
      value: `${stats.avgResponseTime.toFixed(1)}s`,
      icon: Clock,
      color: "purple",
      description: "Tempo de resposta das consultas",
    },
    {
      title: "Taxa de Sucesso",
      value: `${stats.successRate.toFixed(1)}%`,
      icon: Activity,
      color:
        stats.successRate > 95
          ? "green"
          : stats.successRate > 85
          ? "yellow"
          : "red",
      description: "Consultas bem-sucedidas",
    },
    {
      title: "Plataformas Ativas",
      value: `${stats.platformsActive}/3`,
      icon: Users,
      color: stats.platformsActive === 3 ? "green" : "yellow",
      description: "Scholar, Lattes, ORCID",
    },
    {
      title: "Última Atualização",
      value: new Date(stats.lastUpdate).toLocaleDateString("pt-BR"),
      icon: Clock,
      color: "gray",
      description: "Dados mais recentes",
    },
  ];

  return (
    <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
      {statCards.map((card, idx) => {
        const Icon = card.icon;
        const colorClasses = {
          blue: "text-blue-600 bg-blue-100",
          green: "text-green-600 bg-green-100",
          purple: "text-purple-600 bg-purple-100",
          yellow: "text-yellow-600 bg-yellow-100",
          red: "text-red-600 bg-red-100",
          gray: "text-gray-600 bg-gray-100",
        };

        return (
          <div
            key={idx}
            className='bg-white rounded-lg shadow border p-6 hover:shadow-md transition-shadow'
          >
            <div className='flex items-center justify-between mb-4'>
              <div
                className={`p-2 rounded-lg ${
                  colorClasses[card.color as keyof typeof colorClasses]
                }`}
              >
                <Icon className='h-6 w-6' />
              </div>
            </div>

            <h3 className='text-sm font-medium text-gray-500 mb-1'>
              {card.title}
            </h3>
            <p className='text-2xl font-bold text-gray-900 mb-1'>
              {card.value}
            </p>
            <p className='text-sm text-gray-600'>{card.description}</p>

            {/* Indicador de status */}
            {card.title === "Taxa de Sucesso" && (
              <div className='mt-3'>
                <div className='flex items-center mb-1'>
                  <div className='flex-1 bg-gray-200 rounded-full h-2'>
                    <div
                      className={`h-2 rounded-full ${
                        stats.successRate > 95
                          ? "bg-green-500"
                          : stats.successRate > 85
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${stats.successRate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            )}

            {card.title === "Plataformas Ativas" && (
              <div className='mt-3 flex space-x-1'>
                <div
                  className={`w-2 h-2 rounded-full ${
                    stats.platformsActive >= 1 ? "bg-green-400" : "bg-gray-300"
                  }`}
                  title='Google Scholar'
                ></div>
                <div
                  className={`w-2 h-2 rounded-full ${
                    stats.platformsActive >= 2 ? "bg-green-400" : "bg-gray-300"
                  }`}
                  title='Plataforma Lattes'
                ></div>
                <div
                  className={`w-2 h-2 rounded-full ${
                    stats.platformsActive >= 3 ? "bg-green-400" : "bg-gray-300"
                  }`}
                  title='ORCID'
                ></div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default StatsCards;
