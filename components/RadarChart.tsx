'use client'

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'

interface RadarChartProps {
  data: {
    name: string
    value: number
  }[]
}

export default function ArticleRadarChart({ data }: RadarChartProps) {
  return (
    <div className="w-full h-80 bg-neutral-900 rounded-lg p-4 border border-neutral-800">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid stroke="#3f3f46" />
          <PolarAngleAxis 
            dataKey="name" 
            tick={{ fill: '#e5e7eb', fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 5]} 
            tick={{ fill: '#9ca3af', fontSize: 10 }}
          />
          <Radar
            name="評価"
            dataKey="value"
            stroke="#eab308"
            fill="#eab308"
            fillOpacity={0.3}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}

