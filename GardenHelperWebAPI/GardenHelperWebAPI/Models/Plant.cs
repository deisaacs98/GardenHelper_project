using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GardenHelperWebAPI.Models
{
    public class Plant
    {
        public int Id { get; set; }
        public double SpeciesId { get; set; }
        public string CommonName { get; set; }
        public string ImageUrl { get; set; }
        public string DatePlanted { get; set; }
        public string LastWatering { get; set; }
        public string HealthStatus { get; set; }
        public double Height { get; set; }
        public double SoilPH { get; set; }
        public double Light { get; set; }
        public double SoilMoisture { get; set; }
        public bool Edible { get; set; }
        public double? MinTemp { get; set; }
        public double? MaxTemp { get; set; }
        public double? MinPH { get; set; }
        public double? MaxPH { get; set; }
        public int? RequiredLight { get; set; }
        public double? MinPrecipitation { get; set; }
        public double? MaxPrecipitation { get; set; }
        public int? SoilHumidity { get; set; }
        public int? AtmosphericHumidity { get; set; }
        public int GardenerId { get; set; }

    }
}
