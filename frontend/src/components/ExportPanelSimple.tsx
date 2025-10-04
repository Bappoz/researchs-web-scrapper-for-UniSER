/**
 * 📤 PAINEL DE EXPORTAÇÃO SIMPLIFICADO
 * Componente para download de resultados
 */

import React from "react";
import { Download, FileText, Table } from "lucide-react";
import type { SearchResponse } from "../services/api_new";

interface ExportPanelProps {
  results: SearchResponse;
  searchQuery: string;
}

const ExportPanel: React.FC<ExportPanelProps> = ({ results, searchQuery }) => {
  const handleExportCSV = () => {
    // Preparar dados para CSV
    let csvData: any[] = [];

    if (results.data?.publications) {
      csvData = results.data.publications.map((pub: any) => ({
        title: pub.title,
        authors: pub.authors,
        year: pub.year,
        cited_by: pub.cited_by,
        platform: results.platform,
      }));
    } else if (results.data?.lattes_profiles) {
      csvData = results.data.lattes_profiles.map((profile: any) => ({
        name: profile.name,
        institution: profile.current_institution,
        position: profile.current_position,
        publications: profile.total_publications,
        projects: profile.total_projects,
        platform: "lattes",
      }));
    } else if (results.data?.orcid_profiles) {
      csvData = results.data.orcid_profiles.map((profile: any) => ({
        name: `${profile.given_names} ${profile.family_name}`,
        orcid_id: profile.orcid_id,
        works_count: profile.works?.length || 0,
        platform: "orcid",
      }));
    }

    // Gerar CSV
    if (csvData.length > 0) {
      const headers = Object.keys(csvData[0]);
      const csvContent = [
        headers.join(","),
        ...csvData.map((row) =>
          headers.map((header) => `"${row[header] || ""}"`).join(",")
        ),
      ].join("\n");

      // Download
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const link = document.createElement("a");
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute(
        "download",
        `academic_search_${searchQuery.replace(/\s+/g, "_")}_${
          new Date().toISOString().split("T")[0]
        }.csv`
      );
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleExportJSON = () => {
    const jsonContent = JSON.stringify(results, null, 2);
    const blob = new Blob([jsonContent], {
      type: "application/json;charset=utf-8;",
    });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute(
      "download",
      `academic_search_${searchQuery.replace(/\s+/g, "_")}_${
        new Date().toISOString().split("T")[0]
      }.json`
    );
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getResultsCount = () => {
    if (results.data?.publications) return results.data.publications.length;
    if (results.data?.lattes_profiles)
      return results.data.lattes_profiles.length;
    if (results.data?.orcid_profiles) return results.data.orcid_profiles.length;
    if (results.results_by_platform) {
      return Object.values(results.results_by_platform).reduce(
        (total: number, platformData: any) => {
          if (platformData.publications)
            return total + platformData.publications.length;
          if (platformData.lattes_profiles)
            return total + platformData.lattes_profiles.length;
          if (platformData.orcid_profiles)
            return total + platformData.orcid_profiles.length;
          return total;
        },
        0
      );
    }
    return 0;
  };

  const resultsCount = getResultsCount();

  return (
    <div className='bg-white rounded-lg shadow p-4'>
      <h3 className='text-lg font-medium text-gray-900 mb-4'>
        📤 Exportar Resultados
      </h3>

      <div className='space-y-3'>
        <div className='text-sm text-gray-600 mb-4'>
          <p>
            <strong>Busca:</strong> {searchQuery}
          </p>
          <p>
            <strong>Resultados:</strong> {resultsCount}
          </p>
          <p>
            <strong>Plataforma:</strong> {results.platform}
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          disabled={resultsCount === 0}
          className='w-full flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors'
        >
          <Table size={16} />
          <span>Exportar CSV</span>
        </button>

        <button
          onClick={handleExportJSON}
          disabled={resultsCount === 0}
          className='w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors'
        >
          <FileText size={16} />
          <span>Exportar JSON</span>
        </button>

        {results.csv_file && (
          <div className='text-xs text-gray-500 mt-2'>
            <p>✅ Arquivo CSV salvo no servidor: {results.csv_file}</p>
          </div>
        )}

        {results.excel_file && (
          <div className='text-xs text-gray-500 mt-2'>
            <p>✅ Arquivo Excel salvo no servidor: {results.excel_file}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExportPanel;
