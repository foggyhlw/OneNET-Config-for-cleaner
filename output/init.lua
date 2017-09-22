function startup()
    dofile('init_main.lc')
end

--[[
wd_pin=0
gpio.mode(wd_pin,gpio.OUTPUT)
function max813_feed()
    if gpio.read(wd_pin)==0 then
        gpio.write(wd_pin,1)
        return
    end
    if gpio.read(wd_pin)==1 then
        gpio.write(wd_pin,0)
        return
    end
end

tmr.alarm(6,800,tmr.ALARM_AUTO,max813_feed)
--]]
--pms3003_warmup()

tmr.alarm(1,6000,tmr.ALARM_SINGLE,startup)
