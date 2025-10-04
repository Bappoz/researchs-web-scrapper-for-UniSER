/**
 * 📊 CARTÕES DE ESTATÍSTICAS SIMPLIFICADOS
 * Componente para exibir métricas de busca acadêmica
 */

import React from "react";
import {
  TrendingUp,
  Users,
  FileText,
  Clock,
  BookOpen,
  Target,
} from "lucide-react";

interface StatsCardsProps {
  totalPublications: number;
  totalAuthors: number;
  totalProjects: number;
  executionTime: number;
}

const StatsCards: React.FC<StatsCardsProps> = ({
  totalPublications,
  totalAuthors,
  totalProjects,
  executionTime,
}) => {
  const statsData = [
    {
      title: "Publicações",
      value: totalPublications,
      icon: FileText,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
      change: totalPublications > 0 ? "+100%" : "0%",
    },
    {
      title: "Pesquisadores",
      value: totalAuthors,
      icon: Users,
      color: "text-green-600",
      bgColor: "bg-green-100",
      change: totalAuthors > 0 ? "+100%" : "0%",
    },
    {
      title: "Projetos",
      value: totalProjects,
      icon: Target,
      color: "text-purple-600",
      bgColor: "bg-purple-100",
      change: totalProjects > 0 ? "+100%" : "0%",
    },
    {
      title: "Tempo (s)",
      value: Number(executionTime.toFixed(2)),
      icon: Clock,
      color: "text-orange-600",
      bgColor: "bg-orange-100",
      change: executionTime < 5 ? "Rápido" : "Lento",
    },
  ];

  return (
    <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8'>
      {statsData.map((stat, index) => {
        const IconComponent = stat.icon;
        return (
          <div
            key={index}
            className='bg-white rounded-lg shadow-md p-6 border border-gray-200'
          >
            <div className='flex items-center justify-between'>
              <div>
                <p className='text-sm font-medium text-gray-600 uppercase tracking-wide'>
                  {stat.title}
                </p>
                <p className='text-2xl font-bold text-gray-900 mt-2'>
                  {typeof stat.value === "number"
                    ? stat.value.toLocaleString()
                    : stat.value}
                </p>
              </div>
              <div className={`${stat.bgColor} ${stat.color} p-3 rounded-full`}>
                <IconComponent size={24} />
              </div>
            </div>
            <div className='mt-4 flex items-center'>
              <TrendingUp size={16} className='text-green-500 mr-1' />
              <span className='text-sm text-green-600 font-medium'>
                {stat.change}
              </span>
              <span className='text-sm text-gray-500 ml-2'>desta busca</span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default StatsCards;
