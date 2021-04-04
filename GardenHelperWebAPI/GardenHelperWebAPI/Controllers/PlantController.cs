using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using GardenHelperWebAPI.Data;
using GardenHelperWebAPI.Models;


namespace GardenHelperWebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PlantController : ControllerBase
    {
        private ApplicationDbContext _context;
        public PlantController(ApplicationDbContext context)
        {
            _context = context;
        }
        // GET Plants in database
        [HttpGet]
        public IActionResult Get()
        {
            var plants = _context.Plants;
            return Ok(plants);
        }
        // GET Plants By Gardener
        [HttpGet("gardener={gardener_id}/index")]
        public IActionResult Get(int gardener_id)
        {
            var plant = _context.Plants.Where(m => m.GardenerId == gardener_id);
            return Ok(plant);
        }

        // GET Logs By Plant
        [HttpGet("plant={plant_id}/index")]
        public IActionResult GetLogs(int plant_id)
        {
            var log = _context.Logs.Where(m => m.PlantId == plant_id);
            return Ok(log);
        }

        // GET EdibleLogs
        [HttpGet("edible={plant_id}/index")]
        public IActionResult GetEdibleLogs(int plant_id)
        {
            var log = _context.EdibleLogs.Where(m => m.PlantId == plant_id);
            return Ok(log);
        }

        [HttpGet("gardener={gardener_id}/plant={id}")]
        public IActionResult Get(int id, int gardener_id)
        {
            var plant = _context.Plants.Where(m => m.Id == id && m.GardenerId == gardener_id);
            return Ok(plant);
        }

        [HttpGet("plant={plant_id}/log={id}")]
        public IActionResult GetLog(int id, int plant_id)
        {
            var log = _context.Logs.Where(m => m.Id == id && m.PlantId == plant_id);
            return Ok(log);
        }

        [HttpGet("plant={plant_id}/ediblelog={id}")]
        public IActionResult GetEdibleLog(int id, int plant_id)
        {
            var log = _context.EdibleLogs.Where(m => m.Id == id && m.PlantId == plant_id);
            return Ok(log);
        }

        [HttpPost("post-plant")]
        public IActionResult Post([FromBody] Plant value)
        {
            _context.Plants.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        [HttpPost("post-log")]
        public IActionResult Post([FromBody] Log value)
        {
            _context.Logs.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        [HttpPost("post-edible-log")]
        public IActionResult Post([FromBody] EdibleLog value)
        {
            _context.EdibleLogs.Add(value);
            _context.SaveChanges();
            return Ok();
        }

        [HttpPut]
        public IActionResult Put([FromBody] Plant plant)
        {
            _context.Plants.Update(plant);
            _context.SaveChanges();
            return Ok();
        }
        [HttpPut]
        public IActionResult Put([FromBody] Log log)
        {
            _context.Logs.Update(log);
            _context.SaveChanges();
            return Ok();
        }
        [HttpPut]
        public IActionResult Put([FromBody] EdibleLog log)
        {
            _context.EdibleLogs.Update(log);
            _context.SaveChanges();
            return Ok();
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            var selectedPlant = _context.Plants.FirstOrDefault(m => m.Id == id);
            _context.Plants.Remove(selectedPlant);
            _context.SaveChanges();
            return Ok();
        }

        [HttpDelete("log/{id}")]
        public IActionResult DeleteLog(int id)
        {
            var selectedLog = _context.Logs.FirstOrDefault(m => m.Id == id);
            _context.Logs.Remove(selectedLog);
            _context.SaveChanges();
            return Ok();
        }

        [HttpDelete("edible-log/{id}")]
        public IActionResult DeleteEdibleLog(int id)
        {
            var selectedLog = _context.EdibleLogs.FirstOrDefault(m => m.Id == id);
            _context.EdibleLogs.Remove(selectedLog);
            _context.SaveChanges();
            return Ok();
        }

    }
}
