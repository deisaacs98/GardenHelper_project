using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GardenHelperWebAPI.Models
{
    public class Log
    {
        public int Id { get; set; }
        public double PlantId { get; set; }
        public string Date { get; set; }
        public string ImageUrl { get; set; }
        public bool WateredToday { get; set; }
        public string HealthStatus { get; set; }
        public double Height { get; set; }
        public double SoilPH { get; set; }
        public double Light { get; set; }
        public double SoilMoisture { get; set; }
        public bool WaterPrediction { get; set; }
        public bool PredictionAccurate { get; set; }

    }
}
