#import <Foundation/Foundation.h>
#include <IOKit/ps/IOPowerSources.h>
#include <IOKit/ps/IOPSKeys.h>

int get_symbol(int *percent, char *symbol) {
    switch(*percent) {
        case 0 ... 9:
            strcpy(symbol, "");
            break;
        case 10 ... 19:
            strcpy(symbol, "");
            break;
        case 20 ... 29:
            strcpy(symbol, "");
            break;
        case 30 ... 39:
            strcpy(symbol, "");
            break;
        case 40 ... 49:
            strcpy(symbol, "");
            break;
        case 50 ... 59:
            strcpy(symbol, "");
            break;
        case 60 ... 69:
            strcpy(symbol, "");
            break;
        case 70 ... 79:
            strcpy(symbol, "");
            break;
        case 80 ... 89:
            strcpy(symbol, "");
            break;
        case 90 ... 95:
            strcpy(symbol, "");
            break;
        case 96 ... 100:
            strcpy(symbol, "");
            break;
        default:
            strcpy(symbol, "");
            break;
    }
    return 1;
}

static int get_battery_info(bool *has_battery, bool *charging) {
    CFTypeRef ps_info = IOPSCopyPowerSourcesInfo();
    CFTypeRef ps_list = IOPSCopyPowerSourcesList(ps_info);

    long ps_count = CFArrayGetCount(ps_list);
    if (!ps_count) return 0;

    int cur_capacity = 0;
    int max_capacity = 0;
    int percent = 0;
    
    for (int i = 0; i < ps_count; ++i) {
        CFDictionaryRef ps = IOPSGetPowerSourceDescription(ps_info, CFArrayGetValueAtIndex(ps_list, i));
        if (!ps) continue;

        CFTypeRef ps_type = CFDictionaryGetValue(ps, CFSTR(kIOPSTypeKey));
        if (!ps_type || !CFEqual(ps_type, CFSTR(kIOPSInternalBatteryType))) continue;

        CFTypeRef ps_cur = CFDictionaryGetValue(ps, CFSTR(kIOPSCurrentCapacityKey));
        if (!ps_cur) continue;

        CFTypeRef ps_max = CFDictionaryGetValue(ps, CFSTR(kIOPSMaxCapacityKey));
        if (!ps_max) continue;

        CFTypeRef ps_charging = CFDictionaryGetValue(ps, CFSTR(kIOPSPowerSourceStateKey));
        if (!ps_charging) continue;

        CFNumberGetValue((CFNumberRef) ps_cur, kCFNumberSInt32Type, &cur_capacity);
        CFNumberGetValue((CFNumberRef) ps_max, kCFNumberSInt32Type, &max_capacity);
        *charging = !CFEqual(ps_charging, CFSTR(kIOPSBatteryPowerValue));
        *has_battery = true;
        percent = (int)((double) cur_capacity / (double) max_capacity * 100);
        break;
    }

    CFRelease(ps_list);
    CFRelease(ps_info);
    return percent;
}

int main() {
    bool has_battery = false;
    bool charging = false;
    int status = 0;
    char *symbol = NULL;

    symbol = malloc(4);
    if (!symbol) {
        NSLog(@"error: could not assign memory");
        exit(EXIT_FAILURE);
    }

    int percent = get_battery_info(&has_battery, &charging);
    if (!has_battery) {
        strcpy(symbol, "");
        exit(EXIT_SUCCESS);
    }
    if (charging) {
        status = 1;
    } 

    int is_symbol = get_symbol(&percent, symbol);
    if (!is_symbol) {
        exit(EXIT_FAILURE);
    } else {
        // add a lightning symbol if battery is being charged
        if (status > 0) {
            strncat(symbol, "", 4);
        }
    }

    printf("%s %d%% \n", symbol, percent);
    exit(EXIT_SUCCESS);
}
