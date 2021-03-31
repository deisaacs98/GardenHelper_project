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
        public string CommonName { get; set; }
        public DateTime DatePlanted { get; set; }
        public DateTime DateHarvested { get; set; }
        public DateTime LastWatering { get; set; }
        public string HealthStatus { get; set; }
        public double Height { get; set; }
        public double SoilPH { get; set; }
        public double Light { get; set; }
        public double SoilMoisture { get; set; }
        public double AmountHarvested { get; set; }

        public int GardenerId { get; set; }

    }
}
